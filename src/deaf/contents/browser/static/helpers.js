
(function ($) {
    var SLIDESHOW_TIMEOUT = 5000;

    var Timer = function(callback) {
        var timeout = null;
        return {
            start: function() {
                this.pause();
                timeout = setTimeout(this.next, SLIDESHOW_TIMEOUT);
            },
            next: function() {
                timeout = null;
                callback();
                this.start();
            },
            pause: function() {
                if (timeout !== null) {
                    clearTimeout(timeout);
                    timeout = null;
                }
            }

        };
    };

    var make_slideshow = function($container) {
        if (!$container.length) {
            return;
        };
        var $slideshow = $container.children('.slideshow');
        var $images = $slideshow.children();
        var $controls = $container.children('.navigation').children();
        // Current selected elements
        var $current_image = $images.first();
        var $current_control = $controls.first();
        var active = false;

        // Activate them
        $current_image.show();
        $current_control.addClass('current');

        // Define a method to switch to a next one.
        var switch_to = function($following_image, $following_control) {
            if (!active) {
                active = true;

                $current_control.removeClass('current');
                return $.when(
                    $current_image.fadeOut().promise(),
                    $following_image.fadeIn().promise()
                ).done(function () {
                    $current_image = $following_image;
                    $current_control = $following_control;
                    $current_control.addClass('current');
                    active = false;
                });
            };
            return $.Deferred().resolve();
        };

        var timer = Timer(function() {
            var $following_image = $current_image.next();
            var $following_control = $current_control.next();
            if (!$following_image.length) {
                $following_image = $images.first();
            };
            if (!$following_control.length) {
                $following_control = $controls.first();
            };
            return switch_to($following_image, $following_control);
        });

        // On click of a control, go to the corresponding image.
        $container.delegate('.control', 'click', function() {
            switch_to($($images.get($controls.index(this))), $(this));
            timer.start();
        });

        // On hover, we pause and hide the mask
        $slideshow.hover(
            function() {
                timer.pause();
                $current_image.children('.carousel-mask').fadeOut();
            }, function() {
                $current_image.children('.carousel-mask').fadeIn();
                timer.start();
            });

        // Start the timeout
        timer.start();
    };


    $(document).ready(function() {

        // Home slideshow
        make_slideshow($('.homepage-slideshow'));

        // Page Related
        $('.page-tabs').tabs(
            '.page-tabs dd',
            {tabs: 'dt', effect:'slide', initialIndex: null});

        // Buy ticket popup
        var loaded = false;
        $('a#ticket-trigger').bind('click', function() {
            if (!loaded) {
                // Load the iframe at the last minute.
                $('div#ticket-frame iframe').attr('src', $(this).attr('href'));
                loaded = true;
            };
        }).overlay({
            oneInstance: false,
            top: 0,
            left: 250
        });
    });
})(jQuery);
