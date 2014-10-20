from django.test import TestCase
from django.test.client import Client

from django.core.management import call_command
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from services.models import (
    Service,
    ServiceSubscription, 
    ServiceSubscriptionPayment, 
    DATE_CHOICES,
    UNIT_MONTHS
)

from invoice.models import Customer

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

    DATE_FMT = '%Y-%m-%d %H:%M:%S+00:00'
    DATE_FMT_YMG = '%Y-%m-%d'

    def setUp(self):
        """
        """
        super(TestCaseWithFixtures, self).setUp()
        call_command('loaddata', 'fixtures/test_data.json', verbosity=0)
                
                
class ServiceSubscriptionPaymentTest(TestCaseWithFixtures):
    ''' '''

    def setUp(self):
        super(ServiceSubscriptionPaymentTest, self).setUp()

        self.customer = Customer.objects.first()
        self.service = Service.objects.first()
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
        """
        """

        response = self._POST(
            reverse('admin:services_servicesubscriptionpayment_delete', args=(sub_payment.pk,)),
            ajax,
            **kwargs
        )
        #TESTING delete_payments action --> TODO: is there a way to reverse it?
        sub_payment.delete()
        return response

    def _do_POST_service_subscripton_payment_create(self, ajax=False, **kwargs):
        """
        """

        response = self._POST(
            reverse('admin:services_servicesubscriptionpayment_add', args=()),
            ajax,
            **kwargs
        )
        return response

    def _do_POST_service_subscripton_delete(self, subscription, ajax=False, **kwargs):
        """
        """

        response = self._POST(
            reverse('admin:services_servicesubscription_delete', args=(subscription.pk,)),
            ajax,
            **kwargs
        )
        #TODO: here delete_subscriptions admin action should be tested
        return response

    def _do_POST_service_subscripton_create(self, ajax=False, **kwargs):
        """
        """

        response = self._POST(
            reverse('admin:services_servicesubscription_add', args=()),
            ajax,
            **kwargs
        )
        return response

    def _do_POST_service_delete(self, service, ajax=False, **kwargs):
        """
        """

        response = self._POST(
            reverse('admin:services_service_delete', args=(service.pk,)),
            ajax,
            **kwargs
        )
        return response

    def _do_POST_service_create(self, ajax=False, **kwargs):
        """
        """

        response = self._POST(
            reverse('admin:services_service_add', args=()),
            ajax,
            **kwargs
        )
        return response

    def test_client_service_create(self, query_string=""):
        """
        """
     
        # login with client
        logged_in = self._admin_login()

        self.assertTrue(logged_in)

        last_serv_pk = Service.objects.count()

        response = self._do_POST_service_create(
            abbreviation = "serv",
            name = "Servizio test",
            description = "Servizio di test",
            period = 12,
            period_unit_raw = UNIT_MONTHS,
            period_unit_display = UNIT_MONTHS,
            amount = 40,
            default_vat_percent = 0.22,
        )

        if logged_in:
            self._check_for_redirect_response(response,is_ajax=False)

            try:
                service = Service.objects.get(
                    pk=last_serv_pk+1
                )
            except Service.DoesNotExist as e:
                service = False

            self.assertTrue(service)

        else:
            self._check_for_redirect_response(response)

    def test_client_service_subscripton_create(self, query_string=""):
        """
        """
     
        # login with client
        logged_in = self._admin_login()

        self.assertTrue(logged_in)

        last_sub_pk = ServiceSubscription.all_objects.count()

        customer = self.customer.pk
        service = self.service.pk
        response = self._do_POST_service_subscripton_create(
            customer = customer,
            service = service,
            amount = 23,
            vat_percent = 0.22,
            discount = 0,
            invoice_period = 12,
            subscribed_on_0 = DATE_CHOICES[14][0].strftime(self.DATE_FMT_YMG), 
            subscribed_on_1 = "00:00:00", 
            subscribed_until = DATE_CHOICES[15][0].strftime(self.DATE_FMT),
            note = "note",
        )

        if logged_in:
            self._check_for_redirect_response(response,is_ajax=False)

            try:
                subscription = ServiceSubscription.objects.get(
                    pk=last_sub_pk+1
                )
            except ServiceSubscription.DoesNotExist as e:
                subscription = False

            self.assertTrue(subscription)


        else:
            self._check_for_redirect_response(response)

    def test_client_service_subscripton_payment_create(self, query_string=""):
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

        else:
            self._check_for_redirect_response(response)

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

        print response

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
            self.assertEqual(self.payment.paid_for.replace(tzinfo=pytz.UTC),updated_subscription.last_paid_for) 
        else:
            self._check_for_redirect_response(response)
