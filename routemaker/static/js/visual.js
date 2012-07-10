var Visual = function() {
    // Configura o efeito do menu com as opções do usuário autenticado.
    this.configUserMenuOptions = function() {
        $('.dropdown-toggle').click(function (e) {
            e.preventDefault();
            $('ul.dropdown-menu').toggle();
        });
    }
    
    // Remove um item do resultado da lista de pedidos.
    this.removeSortableItem = function(itemId) {
        $('#' + itemId).remove(); 
        $('#pedidos-placeholder').sortable('refresh');
    }
}

var visual = new Visual();