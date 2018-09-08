$(document).ready(function() {
  $("a[data-toggle='modal']").click(function() {
    $($(this).attr('href')).addClass('is-active');
  });

  $("a.delete").click(function() {
    $(this).parents('div.modal').removeClass('is-active');
  });

  $("a.navbar-burger").click(function() {
    $("div.navbar-menu").toggleClass('is-active');
  });
});