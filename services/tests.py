from django.test import TestCase
from django.test.client import Client

from django.core.management import call_command
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from services.models import ServiceSubscription, ServiceSubscriptionPayment, DATE_CHOICES

from lib import views_support
import pytz
import datetime
#from django.utils import timezone

# Create your tests here.

class TestWithClient(TestCase):

    ADMIN_USERNAME = "admin"
    ADMIN_TEST_PASSWORD = "admin"

    def setUp(self):

        # Create test user
        self._user = self.create_admin_user(username=self.ADMIN_USERNAME)

        self._c = Client()

    def create_admin_user(self, username=None):
        """Make the user able to login."""
        user = User.objects.create(
            username=[self.ADMIN_USERNAME, username][bool(username)]
        )
        user.set_password(self.ADMIN_TEST_PASSWORD)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def create_user_unloggable(self, username=None):
        """Create user with no password --> cannot login"""
        user = User.objects.create(
            username=[self.ADMIN_USERNAME, username][bool(username)]
        )
        return user

    def _logout(self):
        self._c.logout()

    def _admin_login(self, user=None):
        """Login a user.

        If user is None, login the default user
        """
        self._logout()
        login_user = [self._user, user][bool(user)]
        rv = self._c.login(username=login_user.username, password=self.ADMIN_TEST_PASSWORD)

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
        self.subscription = ServiceSubscription.objects.first()
        self.payment = ServiceSubscriptionPayment()
        self.payment.subscription = self.subscription
        self.payment.amount = self.subscription.service.amount
        self.payment.vat_percent = self.subscription.vat_percent
        self.payment.discount = self.subscription.discount
        #date = DATE_CHOICES[9][0].strftime(self.DATE_FMT)
        #date_aw = timezone.datetime(int(date[:4]),int(date[6:7]),int(date[9:10]),tzinfo=pytz.UTC)
        #self.payment.paid_for = date_aw
        self.payment.paid_for = DATE_CHOICES[9][0]
        self.payment.note = "note"
        self.payment.save()
        self.subscription.last_paid_on = self.payment.paid_on
        self.subscription.last_paid_for = self.payment.paid_for
        self.subscription.save()

    def _do_POST_service_subscripton_payment_delete(self, sub_payment, ajax=False, **kwargs):

        response = self._POST(
            reverse('admin:services_servicesubscriptionpayment_delete', args=(sub_payment.pk,)),
            ajax,
            **kwargs
        )
        #TESTING delete_payments action --> TODO: is there a way to reverse it?
        sub_payment.delete()
        return response

    def _do_POST_service_subscripton_payment_create(self, ajax=False, **kwargs):

        response = self._POST(
            reverse('admin:services_servicesubscriptionpayment_add', args=()),
            ajax,
            **kwargs
        )
        return response

    def test_client_service_subscripton_payment_delete(self, payment=None, query_string=""):
        """
        """
     
        # login with client
        logged_in = self._admin_login()

        self.assertTrue(logged_in)

        #last_payment = ServiceSubscriptionPayment.objects.order_by("-id").first
        customer = self.subscription.customer.pk
        service = self.subscription.service.pk
        response = self._do_POST_service_subscripton_payment_create(
            customer = customer,
            service = service,
            amount = self.subscription.service.amount,
            vat_percent = self.subscription.vat_percent,
            discount = self.subscription.discount,
            paid_for = DATE_CHOICES[10][0].strftime(self.DATE_FMT),
            #paid_for = DATE_CHOICES[10][0],
            note = "note",
        )

        if logged_in:
            self._check_for_redirect_response(response,is_ajax=False)

            try:
                sub_payment = ServiceSubscriptionPayment.objects.get(
                    pk=self.payment.pk+1
                )
            except ServiceSubscriptionPayment.DoesNotExist as e:
                sub_payment = False

            self.assertTrue(sub_payment)

            updated_subscription = ServiceSubscription.objects.get(pk=self.subscription.pk)
            self.assertEqual(sub_payment.paid_on,updated_subscription.last_paid_on) 
            self.assertEqual(sub_payment.paid_for,updated_subscription.last_paid_for) 

            response = self._do_POST_service_subscripton_payment_delete(
                sub_payment)

            self._check_for_success_response(response,is_ajax=False)

            updated_subscription = ServiceSubscription.objects.get(pk=self.subscription.pk)
            self.assertEqual(self.payment.paid_on,updated_subscription.last_paid_on)
            diff = self.payment.paid_for.replace(tzinfo=pytz.UTC) - updated_subscription.last_paid_for
            self.assertEqual(datetime.timedelta(hours=1),diff)
            #self.assertEqual(self.payment.paid_for.replace(tzinfo=pytz.UTC),updated_subscription.last_paid_for) 
        else:
            self._check_for_redirect_response(response)
