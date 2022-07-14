// form input (Materialize)
$(document).ready(function () {
  $('select').formSelect();
});

// Modal trigger (Materialize)
$(document).ready(function () {
  $('.modal').modal();
});

// ===========================================================================


// Hide reviews on main page on page load
$(document).ready(function () {
  $('.show-review').hide();
  $('.close-reviews').hide();
});

// // Show reviews on button click.
// $(document).ready(function(){
//   $('.open-reviews').click(function(){
//     $('.show-review').show();
//     $('.open-reviews').hide();
//     $('.close-reviews').show();
//   });
// });

// // Hide reviews on button click.
// $(document).ready(function(){
//   $('.close-reviews').click(function(){
//     $('.show-review').hide();
//     $('.close-reviews').hide();
//     $('.open-reviews').show();
//   })
// })

// Show reviews on button click.
$(document).ready(function () {
  $(".open-reviews").click(function () {
    $(".show-review").fadeIn(1000);
    $('.open-reviews').hide();
    $('.close-reviews').show();
  });
});

// Hide reviews on button click
$(document).ready(function () {
  $(".close-reviews").click(function () {
    $(".show-review").fadeOut(1000);
    $(".open-reviews").show();
    $('.close-reviews').hide();
  });
});

// Menu tab enlarges on mouse over
// $(document).ready(function () {
//   $('.flash-messages').mouseover(function () {
//     $('.flash-messages').css("text-shadow", "20px");
//   })
//   $('.flash-messages').mouseout(function () {
//     $('.flash-messages').css("background-color", "grey");
//   })
// })