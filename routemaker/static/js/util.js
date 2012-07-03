var Util = function() {
    // A W3C não aceita mais o atributo "target" em links (tag <a>) em doctypes XHTML 1.0 Strict
    // A função abaixo faz com que todos os links que possuem rel="externo" no link, abram em outra janela.
    this.createExternalLinks = function() {
        $('a[rel*=externo]').click(function() {
            window.open(this.href);
            return false;
        });
    }

    // Configura o efeito do menu com as opções do usuário autenticado.
    this.configUserMenuOptions = function() {
        $('.dropdown-toggle').click(function (e) {
            e.preventDefault();
            $('ul.dropdown-menu').toggle();
        });
    }
};

var util = new Util();