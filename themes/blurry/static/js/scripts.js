$.fn.rotate = function(start, stop) {
    return this.each(function() {
        var elem = $(this);
        $({rotate: start}).animate({rotate: stop}, {
            step: function(state) {
                elem.css('transform', 'rotate(' + state + 'deg)');
            }
        });
    });
};

(function ($, root, undefined) {
    $(function () {
        'use strict';

        // DOM ready, take it away

        $('.collapse-button').click(function() {
            var elem=$(this), aside = $('aside');
            if(aside.hasClass('collapsed')) {
                elem.rotate(0, 180);
                aside.hide().removeClass('collapsed').show(400);
            } else {
                elem.rotate(180, 360);
                aside.hide(400, function() {
                    aside.addClass('collapsed').css('display', '');
                });
            }
        });

        $('<section>').attr({
            id: 'tweets'
        }).append(
            $('<header>').text('Tweets')
        ).append(
            $('<div>').html(
                '<p><i class="fa fa-spinner fa-spin"></i> Loading...</p>'
            ).lifestream({
                classname: 'fa-ul',
                limit: 7,
                list: [
                    {
                        service: 'twitter',
                        user: 'iksteen',
                        template: {
                            posted: '<a class="fa-li fa fa-twitter" href="${complete_url}"></a> {{html tweet}}'
                        }
                    }
                ]
            })
        ).prependTo($('aside'));
    });
})(jQuery, this);
