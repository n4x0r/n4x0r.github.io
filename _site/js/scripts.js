$(document).ready(function () {

    $('.archive-title').click(function (e) {
        e.preventDefault();
        var lista = $(e.target).parent().next('.archive-list');
        var icono = $(e.target).parent().children('.glyphicon');
        if (lista && icono) {
            if (lista.css('display') != 'none') {
                lista.hide();
                icono.removeClass('glyphicon-chevron-down');
                icono.addClass('glyphicon-chevron-right');
            } else {
                lista.show();
                icono.removeClass('glyphicon-chevron-right');
                icono.addClass('glyphicon-chevron-down');
            }
        }
    });

});