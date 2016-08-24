from django.test import TestCase
from django.utils import timezone
from utils import update_departures, UnexpectedStatusException
from models import Departure

class UpdateDeparturesTests(TestCase):

    def setUp(self):
        self.basic_response = [['1471984921', 'North Station', '193', 'Beverly', '1471984800', '0', '2', 'Departed'],
            ['1471984921', 'North Station', '329', 'Lowell', '1471985100', '0', '8', 'Now Boarding'],
            ['1471984921', 'North Station', '293', 'Reading', '1471985280', '0', '4', 'Now Boarding'],
            ['1471984921', 'North Station', '117', 'Rockport', '1471986000', '0', '', 'On Time'],
            ['1471984921', 'North Station', '419', 'Fitchburg', '1471986000', '0', '', 'On Time'],
            ['1471984921', 'North Station', '331', 'Lowell', '1471986600', '0', '', 'On Time'],
            ['1471984921', 'North Station', '169', 'Newburyport', '1471986900', '0', '', 'On Time'],
            ['1471984921', 'North Station', '215', 'Haverhill', '1471986900', '0', '', 'On Time'],
            ['1471984921', 'North Station', '119', 'Rockport', '1471987800', '0', '', 'On Time'],
            ['1471984921', 'North Station', '333', 'Lowell', '1471988100', '0', '', 'On Time'],
            ['1471984921', 'North Station', '421', 'Fitchburg', '1471988100', '0', '', 'On Time'],
            ['1471984921', 'North Station', '217', 'Haverhill', '1471988100', '0', '', 'On Time'],
            ['1471984921', 'North Station', '171', 'Newburyport', '1471988400', '0', '', 'On Time'],
            ['1471984921', 'North Station', '335', 'Lowell', '1471989000', '0', '', 'On Time'],
            ['1471984921', 'North Station', '423', 'Fitchburg', '1471989300', '0', '', 'On Time'],
            ['1471984921', 'North Station', '173', 'Newburyport', '1471989900', '0', '', 'On Time'],
            ['1471984921', 'North Station', '295', 'Reading', '1471989900', '0', '', 'On Time'],
            ['1471984921', 'North Station', '337', 'Lowell', '1471991100', '0', '', 'On Time'],
            ['1471984921', 'South Station', '019', 'Middleboro/ Lakeville', '1471984800', '0', '12', 'Departed'],
            ['1471984921', 'South Station', '717', 'Forge Park / 495', '1471985100', '0', '6', 'Now Boarding'],
            ['1471984921', 'South Station', '617', 'Needham Heights', '1471985100', '360', '', 'Delayed'],
            ['1471984921', 'South Station', '083', 'Greenbush', '1471985520', '0', '13', 'Now Boarding'],
            ['1471984921', 'South Station', '823', 'Providence', '1471985700', '0', '', 'On Time'],
            ['1471984921', 'South Station', '775', 'Readville', '1471986000', '0', '', 'On Time'],
            ['1471984921', 'South Station', '045', 'Kingston', '1471986000', '0', '', 'On Time'],
            ['1471984921', 'South Station', '745', 'Walpole', '1471986180', '0', '', 'On Time'],
            ['1471984921', 'South Station', '521', 'Worcester / Union Station', '1471986300', '0', '', 'On Time'],
            ['1471984921', 'South Station', '021', 'Middleboro/ Lakeville', '1471986720', '0', '', 'On Time'],
            ['1471984921', 'South Station', '917', 'Stoughton', '1471986780', '0', '', 'On Time'],
            ['1471984921', 'South Station', '593', 'Framingham', '1471986900', '0', '', 'On Time'],
            ['1471984921', 'South Station', '085', 'Greenbush', '1471987200', '0', '', 'On Time'],
            ['1471984921', 'South Station', '719', 'Forge Park / 495', '1471987200', '0', '', 'On Time'],
            ['1471984921', 'South Station', '619', 'Needham Heights', '1471987620', '0', '', 'On Time'],
            ['1471984921', 'South Station', '047', 'Kingston', '1471988280', '0', '', 'On Time'],
            ['1471984921', 'South Station', '825', 'Wickford Junction', '1471988400', '0', '', 'On Time'],
            ['1471984921', 'South Station', '523', 'Worcester / Union Station', '1471988400', '0', '', 'On Time']]

    def test_create_departures(self):
        update_departures(self.basic_response)
        self.assertEqual(Departure.objects.count(), 36) 

    def test_update_departures(self):
        update_departures(self.basic_response)
        dep = Departure.objects.get(trip=523)
        self.assertEqual(dep.status, dep.STATUS_ON_TIME)
        update_departures([['1471984922', 'South Station', '523', 'Worcester / Union Station', '1471988400', '100', '', 'Delayed']])
        dep = Departure.objects.get(trip=523)
        self.assertEqual(dep.status, dep.STATUS_DELAYED)
        self.assertEqual(dep.lateness, timezone.timedelta(seconds=100))

    def test_deactivate(self):
        update_departures(self.basic_response)
        self.assertEqual(Departure.objects.filter(active=True).count(), 36)
        update_departures(self.basic_response[:10])
        self.assertEqual(Departure.objects.filter(active=True).count(), 10)

    def test_bad_status(self):
        with self.assertRaises(UnexpectedStatusException):
            update_departures([['1471984922', 'South Station', '523', 'Worcester / Union Station', '1471988400', '100', '', 'Derailed']])
