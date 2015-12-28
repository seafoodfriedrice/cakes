$(document).ready(function() {
  $('select').material_select();
  var $categoryInput = $('.category-input');
  var $subcategoryInput = $('.subcategory-input');
  var $addSubcategoryLink = $('.add-subcategory');

  $(".quantity-btn").on("click", function() {
    var button = $(this);
    var oldValue = button.closest('.quantity-group')
      .find('input#quantity-input').val();
    if (button.text() == "+") {
      var newValue = parseFloat(oldValue) + 1;
    } else {
      if (oldValue > 0) {
        var newValue = parseFloat(oldValue) - 1;
      } else {
        newValue = 0;
      }
    }
    button.closest('.quantity-group')
      .find('input#quantity-input').val(newValue);
  });

  var $categories = $('select#category');
  var $subCategories = $('select#sub_category');
  var $categorySelectedOption = $('option:selected', $categories);
  var createSelectOption = function(value, item) {
    if (typeof(value) === 'undefined') {
      value = '';
    }
    if (typeof(item) === 'undefined') {
      item = '';
    }
    var option = '<option value="' + value + '">' + item + '</option>';
    return option;
  };
  var getSubCategoriesByCategoryId = function(categoryId) {
    var result = $.ajax({
      url: "/api/categories/" + categoryId + "/subcategories",
      dataType: "json",
      type: "GET"
    })
    .done(function(result) {
      $subCategories.html('');
      if (result.length) {
        $.each(result, function(i, item) {
          $subCategories.append(createSelectOption(item.id, item.name));
          $subCategories.prop('disabled', false);
        });
      } else {
        $subCategories.append(createSelectOption());
        $subCategories.prop('disabled', true);
      }
      $subCategories.material_select();
    });
  };
  $categories.change(function() {
      $categorySelectedOption = $('option:selected', $categories);
      getSubCategoriesByCategoryId($categorySelectedOption.val());
      $('span', $addSubcategoryLink).text($categorySelectedOption.text());
      if (! $('input', $subcategoryInput).is(':disabled')) {
        $('input', $categoryInput).val($categorySelectedOption.text());
      }
   });
  // Only load the subcategory through the AJAX request when
  // .onload-subcategory is present on the select form. This prevents the
  // subcategory select from being modified for the product_get() view.
  if ($('.onload-subcategory').length) {
    getSubCategoriesByCategoryId($('option:selected', $categories).val());
    $('span', $addSubcategoryLink).text($categorySelectedOption.text());
  }

  var $closeSubcategoryLink = $('.close-subcategory');
  var $currentSubcategoriesSelect = $('.current-subcategories');
  $addSubcategoryLink.on('click', function() {
    $('input', $categoryInput).val($categorySelectedOption.text())
      .prop('disabled', true);
    $('label', $categoryInput).addClass('active');
    $('input', $subcategoryInput).prop('disabled', false);
    $subcategoryInput.add($closeSubcategoryLink).show()
    $(this).hide();
  });
  $closeSubcategoryLink.on('click', function() {
    $('input', $subcategoryInput).prop('disabled', true);
    $('input', $categoryInput).prop('disabled', false).val('');
    $('label', $categoryInput).removeClass('active');
    $subcategoryInput.hide();
    $addSubcategoryLink.show();
    $(this).hide()
  });
  $('.category-submit').on('click', function() {
    $('input', $categoryInput).prop('disabled', false);
  });

});
