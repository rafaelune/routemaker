var Util = function() {
    /* A W3C n�o aceita mais o atributo "target" em links (tag <a>) em doctypes XHTML 1.0 Strict
    A fun��o abaixo faz com que todos os links que possuem rel="externo" no link, abram em outra janela. */
    this.createExternalLinks = function() {
        $('a[rel*=externo]').click(function() {
            window.open(this.href);
            return false;
        });
    }
};

var util = new Util();