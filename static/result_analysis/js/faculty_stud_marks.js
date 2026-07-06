$(document).ready(function () {
    var current_fs, next_fs, previous_fs;
    var left, opacity, scale;
    var animating;

    function resetFieldsetStyles(fieldset) {
        fieldset.css({
            'position': '',
            'left': '',
            'opacity': '',
            'transform': ''
        }).hide();
    }

    function animateToFieldset(current, next) {
        if (animating) return false;
        animating = true;

        current_fs = current;
        next_fs = next;

        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
        next_fs.show();

        current_fs.animate({
            opacity: 0
        }, {
            step: function (now, mx) {
                scale = 1 - (1 - now) * 0.2;
                left = (now * 50) + "%";
                opacity = 1 - now;
                current_fs.css({
                    'transform': 'scale(' + scale + ')'
                });
                next_fs.css({
                    'left': left,
                    'opacity': opacity
                });
            },
            duration: 800,
            complete: function () {
                resetFieldsetStyles(current_fs);
                animating = false;
            },
            easing: 'easeInOutExpo'
        });
    }

    $(".next").click(function () {
        animateToFieldset($(this).parent(), $(this).parent().next());
    });

    $(".previous").click(function () {
        if (animating) return false;
        animating = true;

        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

        previous_fs.show();
        current_fs.animate({
            opacity: 0
        }, {
            step: function (now, mx) {
                scale = 0.8 + (1 - now) * 0.2;
                left = ((1 - now) * 50) + "%";
                opacity = 1 - now;
                current_fs.css({
                    'left': left
                });
                previous_fs.css({
                    'transform': 'scale(' + scale + ')',
                    'opacity': opacity
                });
            },
            duration: 800,
            complete: function () {
                resetFieldsetStyles(current_fs);
                animating = false;
            },
            easing: 'easeInOutExpo'
        });
    });

    $("#progressbar li").click(function () {
        var index = $(this).index();
        var target_fs = $("fieldset").eq(index);

        if (index > $("fieldset:visible").index()) {
            animateToFieldset($("fieldset:visible"), target_fs);
        } else {
            if (animating) return false;
            animating = true;

            current_fs = $("fieldset:visible");
            previous_fs = target_fs;

            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

            previous_fs.show();
            current_fs.animate({
                opacity: 0
            }, {
                step: function (now, mx) {
                    scale = 0.8 + (1 - now) * 0.2;
                    left = ((1 - now) * 50) + "%";
                    opacity = 1 - now;
                    current_fs.css({
                        'left': left
                    });
                    previous_fs.css({
                        'transform': 'scale(' + scale + ')',
                        'opacity': opacity
                    });
                },
                duration: 10,
                complete: function () {
                    resetFieldsetStyles(current_fs);
                    animating = false;
                },
                easing: 'easeInOutExpo'
            });
        }

        $("#progressbar li").removeClass("active");
        for (var i = 0; i <= index; i++) {
            $("#progressbar li").eq(i).addClass("active");
        }
    });



});

