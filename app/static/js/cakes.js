$(document).ready(function() {


  var $modal = $('#modal-add'),
      $modalTitle = $(".modal-title"),
      $inputs = ['id', 'name', 'color', 'quantity', 'used', 'price'],
      $selects = ['brand_id', 'category_id', 'subcategory_id'],
      $form = $('#modal-add-form');

  addProductModal = function() {
    $modalTitle.text("Add Product");
    $.each($inputs, function(index, value) {
      var $field = $("#" + value);
      $field.val('');
    });
    $.each($selects, function(index, value) {
      var $field = $("#" + value.slice(0, -3));
      $field.val('__None');
      $field.material_select();
    });
    $modal.openModal();
  };

  serializeFormAsJson = function() {
    var $array = $form.serializeArray(),
        json = {};
    $.each($array, function() {
        if (this.value == "__None") {
          this.value = '';
        }
        json[this.name] = this.value || '';
    });
    return json;
  };

  addProductSave = function() {
    var $data = serializeFormAsJson();
    $.ajax({
      url: "/api/products",
      type: "POST", 
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      data: JSON.stringify($data),
      success: function(result) {
        console.log(result);
      }
    });
  };

  updateProductSave = function() {
    var $data = serializeFormAsJson(),
        $id = $('#id').val();
    $.ajax({
      url: "/api/products/" + $id,
      type: "PUT", 
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      data: JSON.stringify($data),
      success: function(updated) {
        console.log(updated);
        $('.product-id-' + $id).find('td.product-quantity')
          .text(updated['quantity']).hide().fadeIn(3000);
        Materialize.toast("Updated quantity to " + updated['quantity'], 5000);
      }
    });
  };

  getProductByIdModal = function(id) {
    $.getJSON("/api/products/" + id, {})
      .done(function(data) {
        $.each($inputs, function(index, value) {
          var $field = $("#" + value),
              $label = $field.next();
          $field.val(data[value]);
          $label.addClass("active");
        });
        $.each($selects, function(index, value) {
          var $field = $("#" + value.slice(0, -3));
          if (value == "subcategory_id" && data[value] == null) {
            $field.val('__None');
          } else {
            $field.val(data[value]);
          }
          $field.material_select();
        });
        $modalTitle.text(data['name']);
        $modal.openModal();
      }).fail(function(xhr, textStatus, error) {
        var err = textStatus + ", " + error;
        console.log("Request Failed: " + err);
    });
  };

  $('select').material_select();
  $categoryInput = $('.category-input');
  $subcategoryInput = $('.subcategory-input');
  $addSubcategoryLink = $('.add-subcategory');

  /*
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
  */

  var $categories = $('select#category'),
      $subCategories = $('select#subcategory'),
      $categorySelectedOption = $('option:selected', $categories),
      createSelectOption = function(value, item) {
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
