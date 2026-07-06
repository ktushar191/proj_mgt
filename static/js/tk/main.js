window.onload = function () {
  'use strict';

  var Cropper = window.Cropper;
  var URL = window.URL || window.webkitURL;
  var container = document.querySelector('.img-container');
  var image = container.getElementsByTagName('img').item(0);
  var download = document.getElementById('download');
  var actions = document.getElementById('actions');
  var dataX = document.getElementById('dataX');
  var dataY = document.getElementById('dataY');
  var dataHeight = document.getElementById('dataHeight');
  var dataWidth = document.getElementById('dataWidth');
  var dataRotate = document.getElementById('dataRotate');
  var dataScaleX = document.getElementById('dataScaleX');
  var dataScaleY = document.getElementById('dataScaleY');
  var lastValidCrop = null;
  var options = {
    aspectRatio: 2 / 1,
    viewMode: 2,
    preview: '.img-preview',
    ready: function (e) {
      console.log(e.type);
    },
    cropstart: function (e) {
      console.log(e.type, e.detail.action);
    },
    cropmove: function (e) {
      console.log(e.type, e.detail.action);
    },
    cropend: function (e) {
      console.log(e.type, e.detail.action);
    },
    crop: function (e) {
      var data = e.detail;
      console.log(e.type);
      dataX.value = Math.round(data.x);
      dataY.value = Math.round(data.y);
      dataHeight.value = Math.round(data.height);
      dataWidth.value = Math.round(data.width);

      var validCrop = true;
      if (e.detail.width < 500) validCrop = false;
      if (e.detail.height < 250) validCrop = false;

      if (validCrop) {
        lastValidCrop = cropper.getData();
        $("#crop_photo_x").val(e.detail.x);
        $("#crop_photo_y").val(e.detail.y);
        $("#crop_photo_width").val(e.detail.width);
        $("#crop_photo_height").val(e.detail.height);
      } else {
        cropper.setData(lastValidCrop);
      }
    },
    zoom: function (e) {
      console.log(e.type, e.detail.ratio);
    }
  };
  var optionsLogo = {
    aspectRatio: 1 / 1,
    viewMode: 2,
    preview: '.img-preview',
    ready: function (e) {
      console.log(e.type);
    },
    cropstart: function (e) {
      console.log(e.type, e.detail.action);
    },
    cropmove: function (e) {
      console.log(e.type, e.detail.action);
    },
    cropend: function (e) {
      console.log(e.type, e.detail.action);
    },
    crop: function (e) {
      var data = e.detail;

      console.log(e.type);
      dataX.value = Math.round(data.x);
      dataY.value = Math.round(data.y);
      dataHeight.value = Math.round(data.height);
      dataWidth.value = Math.round(data.width);

      var validCrop = true;
      if (e.detail.width < 500) validCrop = false;
      if (e.detail.height < 250) validCrop = false;

      if (validCrop) {
        lastValidCrop = cropper.getData();
        $("#crop_photo_x").val(e.detail.x);
        $("#crop_photo_y").val(e.detail.y);
        $("#crop_photo_width").val(e.detail.width);
        $("#crop_photo_height").val(e.detail.height);
      } else {
        cropper.setData(lastValidCrop);
      }
    },
    zoom: function (e) {
      console.log(e.type, e.detail.ratio);
    }
  };
  var cropper = new Cropper(image, options);
  var originalImageURL = image.src;
  var uploadedImageType = 'image/jpeg';
  var uploadedImageName = 'cropped.jpg';
  var uploadedImageURL;

  // Tooltip
  $('[data-toggle="tooltip"]').tooltip();

  // Buttons
  if (!document.createElement('canvas').getContext) {
    $('button[data-method="getCroppedCanvas"]').prop('disabled', true);
  }

  if (typeof document.createElement('cropper').style.transition === 'undefined') {
    $('button[data-method="rotate"]').prop('disabled', true);
    $('button[data-method="scale"]').prop('disabled', true);
  }



  // Options
  actions.querySelector('.docs-toggles').onchange = function (event) {
    var e = event || window.event;
    var target = e.target || e.srcElement;
    var cropBoxData;
    var canvasData;
    var isCheckbox;
    var isRadio;

    if (!cropper) {
      return;
    }

    if (target.tagName.toLowerCase() === 'label') {
      target = target.querySelector('input');
    }

    isCheckbox = target.type === 'checkbox';
    isRadio = target.type === 'radio';

    if (isCheckbox || isRadio) {
      if (isCheckbox) {
        options[target.name] = target.checked;
        cropBoxData = cropper.getCropBoxData();
        canvasData = cropper.getCanvasData();

        options.ready = function () {
          console.log('ready');
          cropper.setCropBoxData(cropBoxData).setCanvasData(canvasData);
        };
      } else {
        options[target.name] = target.value;
        options.ready = function () {
          console.log('ready');
        };
      }

      // Restart
      cropper.destroy();
      cropper = new Cropper(image, options);
    }
  };

  // Methods
  actions.querySelector('.docs-buttons').onclick = function (event) {
    var e = event || window.event;
    var target = e.target || e.srcElement;
    var cropped;
    var result;
    var input;
    var data;

    if (!cropper) {
      return;
    }

    while (target !== this) {
      if (target.getAttribute('data-method')) {
        break;
      }

      target = target.parentNode;
    }

    if (target === this || target.disabled || target.className.indexOf('disabled') > -1) {
      return;
    }

    data = {
      method: target.getAttribute('data-method'),
      target: target.getAttribute('data-target'),
      option: target.getAttribute('data-option') || undefined,
      secondOption: target.getAttribute('data-second-option') || undefined
    };

    cropped = cropper.cropped;
    if (data.method) {
      if (typeof data.target !== 'undefined') {
        input = document.querySelector(data.target);

        if (!target.hasAttribute('data-option') && data.target && input) {
          try {
            data.option = JSON.parse(input.value);
          } catch (e) {
            console.log(e.message);
          }
        }
      }

      switch (data.method) {
        case 'rotate':
          if (cropped && options.viewMode > 0) {
            cropper.clear();
          }
          break;
        case 'getCroppedCanvas':
          try {
            data.option = JSON.parse(data.option);
          } catch (e) {
            console.log(e.message);
          }

          if (uploadedImageType === 'image/jpeg') {
            if (!data.option) {
              data.option = {};
            }

            data.option.fillColor = '#fff';
          }

          break;
      }

      result = cropper[data.method](data.option, data.secondOption);
      switch (data.method) {
        case 'rotate':
          if (cropped && options.viewMode > 0) {
            cropper.crop();
          }

          break;

        case 'scaleX':
        case 'scaleY':
          target.setAttribute('data-option', -data.option);
          break;

        case 'getCroppedCanvas':
          if (result) {
            if (!download.disabled) {
              if(photo_selection == 'event'){
                var dataX = ($('#dataX').val() / image.width) * 100;
                var dataY = ($('#dataY').val() / image.height) * 100;
                $('#dataX').val(dataX)
                $('#dataY').val(dataY)
                download.download = uploadedImageName;
                download.href = result.toDataURL(uploadedImageType);
                $('.image_error_text').css('display', 'none')
                $('.outerDivImage').removeClass('error');
                $('.selectedImageHide').css('display', 'none')
                $('.cropImageContain').css('background-image', 'url("' + download.href + '")');
                $('#imageData').val(download.href);
                $('#imageLogoDataUpdate').val(download.href);    
                //showhideprevdiv();
              }else{
                $('#dataLogoX').val(dataX)
                $('#dataLogoY').val(dataY)
                download.download = uploadedImageName;
                download.href = result.toDataURL(uploadedImageType);
                $('#selectedLogo').attr("src",download.href);
                $('#imageLogoData').val(download.href);
                $('#imageLogoDataUpdate').val(download.href);       
                if (typeof ul !== 'undefined' && ul) 
                  $("#upload_logo").click();
              }
            }
          }

          break;

        case 'destroy':
          cropper = null;

          if (uploadedImageURL) {
            URL.revokeObjectURL(uploadedImageURL);
            uploadedImageURL = '';
            image.src = originalImageURL;
          }

          break;
      }

      if (typeof result === 'object' && result !== cropper && input) {
        try {
          input.value = JSON.stringify(result);
        } catch (e) {
          console.log(e.message);
        }
      }
    }
  };

  document.body.onkeydown = function (event) {
    var e = event || window.event;

    if (e.target !== this || !cropper || this.scrollTop > 300) {
      return;
    }

    switch (e.keyCode) {
      case 37:
        e.preventDefault();
        cropper.move(-1, 0);
        break;

      case 38:
        e.preventDefault();
        cropper.move(0, -1);
        break;

      case 39:
        e.preventDefault();
        cropper.move(1, 0);
        break;

      case 40:
        e.preventDefault();
        cropper.move(0, 1);
        break;
    }
  };
  // Import image
  var inputImage = document.getElementById('inputImage');
  var logoImage = document.getElementById('logoImage');
  if (URL) {
    inputImage.onchange = function () {
      var files = this.files;
      var file;

      if (files && files.length) {
        file = files[0];
        const fsize = file.size;
        const fileSize = Math.round((fsize / 1024));
        if (/^image\/\w+/.test(file.type)) {
          if(file.type == 'image/gif'){
            $('.image_error_text').html('Please Select  File Format- JPEG, PNG Ideal image ratio is 2:1');
            $('.image_error_text').css('display', 'block')
         
            image.src = uploadedImageURL = '';
            cropper.destroy();
            cropper = new Cropper(image, optionsLogo);
            $(".innerDIv").css('display', 'none');
            $("#overlayImage").css('display', 'none');
          }else{
          // The size of the file. 
          if (fileSize >= 5096) {
            $('.image_error_text').html('Please Select image less than 5 MB');
            $('.image_error_text').css('display', 'block')
            $('.outerDivImage').addClass('error')
            $('.outerDivImage').css('background-image', 'none');
            $('.selectedImageHide').css('display', 'block')
            $('.img-container').css("display", 'none');
            image.src = uploadedImageURL = '';
            cropper.destroy();
            cropper = new Cropper(image, options);
            $(".innerDIv").css('display', 'none');
            $("#overlayImage").css('display', 'none');
          } else {
            uploadedImageType = file.type;
            uploadedImageName = file.name;
            if (uploadedImageURL) {
              URL.revokeObjectURL(uploadedImageURL);
            }
            image.src = uploadedImageURL = URL.createObjectURL(file);
            cropper.destroy();
            cropper = new Cropper(image, options);
            $(".innerDIv").css('display', 'flex');
            $("#overlayImage").css('display', 'flex');
            $('.img-container').css("display", 'flex');
            //inputImage.value = null;
          }
        }
        } else {
          $('.image_error_text').html('Please Select  File Format- JPEG, PNG Ideal image ratio is 2:1');
          $('.image_error_text').css('display', 'block')
          $('.outerDivImage').addClass('error')
          $('.outerDivImage').css('background-image', 'none');
          $('.selectedImageHide').css('display', 'block')
          $(".innerDIv").css('display', 'none');
          $("#overlayImage").css('display', 'none');
        }

      }
    };

    logoImage.onchange = function () {
    
      var files = this.files;
      var file;
      if (files && files.length) {
        file = files[0];
        const fsize = file.size;
        const fileSize = Math.round((fsize / 1024));
        if (/^image\/\w+/.test(file.type)) {
          // The size of the file. 
          if(file.type == 'image/gif'){
            $('#image_error_text_broadcast').html('Please Select image JPEG,PNG or JPG');
            $('#image_error_text_broadcast').css('display', 'block')
         
            image.src = uploadedImageURL = '';
            cropper.destroy();
            cropper = new Cropper(image, optionsLogo);
            $(".innerDIv").css('display', 'none');
            $("#overlayImage").css('display', 'none');
          }else{
          if (fileSize >= 5096) {
            $('#image_error_text_broadcast').html('Please Select image less than 5 MB');
            $('#image_error_text_broadcast').css('display', 'block')
         
            image.src = uploadedImageURL = '';
            cropper.destroy();
            cropper = new Cropper(image, optionsLogo);
            //alert('Please Select image less than 5 MB');
            $(".innerDIv").css('display', 'none');
            $("#overlayImage").css('display', 'none');
          } else {
           
            uploadedImageType = file.type;
            uploadedImageName = file.name;
            
            if (uploadedImageURL) {
              URL.revokeObjectURL(uploadedImageURL);
            }
            image.src = uploadedImageURL = URL.createObjectURL(file);
            cropper.destroy();
            cropper = new Cropper(image, optionsLogo);
            $(".innerDIv").css('top', '45%');
            $(".innerDIv").css('display', 'flex');
            $("#overlayImage").css('display', 'flex');
            $('.img-container').css("display", 'flex');
            $('#image_error_text_broadcast').css('display', 'none')
            //inputImage.value = null;
            if($('#isadmin').val() == 0){
              $(".innerDIv").css('top', '45%');
            }else{
              $(".innerDIv").css('top', '0%');
            }
          }
        }
        } else {
          // $('.image_error_text').html('Please Select  File Format- JPEG, PNG Ideal image ratio is 2:1');
          // $('.image_error_text').css('display', 'block')
          // $('.outerDivImage').addClass('error')
          // $('.outerDivImage').css('background-image', 'none');
          // $('.selectedImageHide').css('display', 'block')
          $(".innerDIv").css('display', 'none');
          $("#overlayImage").css('display', 'none');
        }

      }
    };
    } else {
      inputImage.disabled = true;
      inputImage.parentNode.className += ' disabled';
    }
};
