var Util = function() {
    /* A W3C não aceita mais o atributo "target" em links (tag <a>) em doctypes XHTML 1.0 Strict
    A função abaixo faz com que todos os links que possuem rel="externo" no link, abram em outra janela. */
    this.createExternalLinks = function() {
        $('a[rel*=externo]').click(function() {
            window.open(this.href);
            return false;
        });
    }

    this.createDatePickers = function() {
    	$('input[rel*=datepicker]').datepicker({
    		dateFormat: 'dd-mm-yy'
    	});
    }

    this.createSelectables = function() {
    	
    	$('ul[rel*=selectable]').bind("mousedown", function(e) {
  			e.metaKey = true;
		})
		.selectable();
    }
};

var util = new Util();