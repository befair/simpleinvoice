from django.test import TestCase
from django.test.client import Client

from django.core.management import call_command
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from services.models import ServiceSubscription, ServiceSubscriptionPayment, DATE_CHOICES

from lib import views_support

# Create your tests here.

class TestWithClient(TestCase):

    USERNAME = ""
    TEST_PASSWORD = ""

    def setUp(self):

        # Create test user
        self._user = self.create_user(username=self.USERNAME)

        self._c = Client()

    def create_user(self, username=None):
        """Make the user able to login."""
        user = User.objects.create(
            username=[self.USERNAME, username][bool(username)]
        )
        user.set_password(self.TEST_PASSWORD)
        user.save()
        return user

    def create_user_unloggable(self, username=None):
        """Create user with no password --> cannot login"""
        user = User.objects.create(
            username=[self.USERNAME, username][bool(username)]
        )
        return user

    def _logout(self):
        self._c.logout()

    def _login(self, user=None):
        """Login a user.

        If user is None, login the default user
        """

        self._logout()
        login_user = [self._user, user][bool(user)]
        rv = self._c.login(username=login_user.username, password=self.TEST_PASSWORD)
        return rv

    def _check_for_error_response(self, response, e=Exception):
        """HTTP response is always 200, context_data 'http_status_code' tells the truth"""
        self.assertEqual(response.status_code, views_support.HTTP_SUCCESS)
        self.assertEqual(
            response.context_data['http_status_code'], 
            views_support.HTTP_ERROR_INTERNAL
        )
        self.assertEqual(response.context_data['exception_type'], e)

    def _check_for_success_response(self, response, is_ajax=True):
        """HTTP response is always 200, context_data 'http_status_code' tells the truth"""
        if is_ajax:
            self.assertEqual(response.status_code, views_support.HTTP_SUCCESS)
            self.assertEqual(
                response.context_data['http_status_code'], 
                views_support.HTTP_SUCCESS
            )
        else:
            self.assertEqual(response.status_code, views_support.HTTP_SUCCESS)
    
    def _check_for_redirect_response(self,response, is_ajax=False):
        """ HTTP response is 302, in case the server redirects to another page"""
        if is_ajax:
            self.assertEqual(response.status_code, views_support.HTTP_SUCCESS)
            self.assertEqual(
                response.context_data['http_status_code'], 
                views_support.HTTP_REDIRECT
            )
        else:
            self.assertEqual(response.status_code, views_support.HTTP_REDIRECT)

    def _POST(self, url, is_ajax, **kwargs):
        
        if is_ajax:
            response = self._c.post(url,
                kwargs,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        else:
            response = self._c.post(url,
                kwargs
            )
        return response

    def _GET(self, url, is_ajax, **kwargs):

        if is_ajax:
            response = self._c.get(url,
                kwargs,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        else:
            response = self._c.get(url,
                kwargs
            )
        return response

class TestCaseWithFixtures(TestWithClient):
    ''' '''

    DATE_FMT = '%Y-%m-%d %H:%M:%S%Z'

    def setUp(self):
        """
        """
        super(TestCaseWithFixtures, self).setUp()
        call_command('loaddata', 'fixtures/test_data.json', verbosity=0)
                
                
class ServiceSubscriptionPaymentTest(TestCaseWithFixtures):
    ''' '''

    def setUp(self):
        super(ServiceSubscriptionPaymentTest, self).setUp()
        print ServiceSubscription.all_objects.all()
        self.subscription = ServiceSubscription.objects.first()
        self.payment = ServiceSubscriptionPayment()
        self.payment.subscription = self.subscription
        self.payment.amount = self.subscription.service.amount
        self.payment.vat_percent = self.subscription.vat_percent
        self.payment.discount = self.subscription.discount
        self.payment.paid_for = DATE_CHOICES[9][0].strftime(self.DATE_FMT)
        self.payment.note = "note"
        self.payment.save()
        self.subscription.last_paid_on = self.payment.paid_on
        self.subscription.last_paid_for = self.payment.paid_for

    def _do_POST_service_subscripton_payment_delete(self, sub_payment, ajax=False, **kwargs):

        response = self._POST(
            reverse('services_servicesubscriptionpayment_delete', args=(sub_payment.pk,)),
            ajax,
            **kwargs
        )
        return response

    def _do_POST_service_subscripton_payment_create(self, ajax=False, **kwargs):

        response = self._POST(
            reverse('services_servicesubscriptionpayment_add', args=()),
            ajax,
            **kwargs
        )
        return response

    #def test_service_subscripton_payment_delete(self):
    #    """
    #    """
    #   
    #    sub_payment = ServiceSubscriptionPayment()
    #    sub_payment.subscription = self.subscription
    #    sub_payment.amount = self.subscription.service.amount
    #    sub_payment.vat_percent = self.subscription.vat_percent
    #    sub_payment.discount = self.subscription.discount
    #    sub_payment.paid_for = DATE_CHOICES[10][0].strftime(self.DATE_FMT)
    #    sub_payment.note = "note"
    #    sub_payment.save()
    #    self.subscription.last_paid_on = sub_payment.paid_on
    #    self.subscription.last_paid_for = sub_payment.paid_for

    #    self.assertEqual(sub_payment.paid_on,self.subscription.last_paid_on) 
    #    self.assertEqual(sub_payment.paid_for,self.subscription.last_paid_for) 

    #    sub_payment.delete()

    #    self.assertEqual(self.payment.paid_on,self.subscription.last_paid_on) 
    #    self.assertEqual(self.payment.paid_for,self.subscription.last_paid_for) 

    def test_client_service_subscripton_payment_delete(self, payment=None, query_string=""):
        """
        """
      
        self._do_POST_service_subscripton_payment_create(
            subscription = self.subscription,
            amount = self.subscription.service.amount,
            vat_percent = self.subscription.vat_percent,
            discount = self.subscription.discount,
            paid_for = DATE_CHOICES[10][0].strftime(self.DATE_FMT),
            note = "note",
        )

        self.assertEqual(sub_payment.paid_on,self.subscription.last_paid_on) 
        self.assertEqual(sub_payment.paid_for,self.subscription.last_paid_for) 

        self._do_POST_service_subscripton_payment_delete(
            sub_payment)

        self.assertEqual(self.payment.paid_on,self.subscription.last_paid_on) 
        self.assertEqual(self.payment.paid_for,self.subscription.last_paid_for) 
