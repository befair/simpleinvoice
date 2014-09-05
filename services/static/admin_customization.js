$ = django.jQuery;

$(document).ready(function(){

  // works when adding a new item
  if(window.location.href.slice(-4) == 'add/') {

    $('.field-service, .field-amount, .field-vat_percent, .field-discount, .field-paid_for, .field-note').hide();

    // trigger when a customer is selected
    $('#id_customer').change(function(e) {
      // get id of the selected customer
      customer_id = e.target.value;
      // ask the server for the services
      $.get(
        '/api/get-services/'+customer_id+'/',
        function(data) {
          window.services = data;
          // delete all options
          $('#id_service').empty();
          // recreate the options, filtered by customer
          $('#id_service').append('<option value="" selected="selected">---------</option>');
          $.each(data, function(i, s) {
            $('#id_service').append(
              $('<option>').text(s.service_name).val(s.service_id)
            );
          });
          // show service form
          $('.field-service').fadeIn();
          console.log(data);
        }
      );
    });

    // trigger when service is selected
    $('#id_service').change(function(e) {
      service_id = e.target.value;
      s = window.services[service_id]; 
      console.log(service_id, s);
      // populate fields with default values
      $('#id_amount').val(s.amount);
      $('#id_vat_percent').val(s.vat);
      $('#id_discount').val(s.discount);
      // show hidden fields
      // matteo88: for reesmarche vat_percent and discount are hidden
      $('.field-amount, .field-paid_for, .field-note').fadeIn();
    });
  }
});
