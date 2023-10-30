var _window = $(window),
_header = $('.header'),
topBottom;
_window.on('scroll',function(){     
    topBottom = $('.header').height();
    Bottom = $('.back1').height();
    if(_window.scrollTop() > topBottom+Bottom){
        _header.addClass('fixed');   
    }
    else{
        _header.removeClass('fixed');   
    }
});
_window.trigger('scroll');