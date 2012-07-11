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
    
    // Configura o efeito de tabulação.
    this.configTabMenus = function() {
        $('tab-menu a').click(function (e) {
            e.preventDefault();
            $(this).tab('show');
        })
    }
    
    // Efeitos ao mover para primeiro tab na tela
    // de filtro de pedidos.
    this.goToFirstTabFilter = function() {
        $('#lnkTab1').tab('show');
        $('#tab2')
            .removeClass('tab-pane')
            .addClass('d_n');
    }
    
    // Efeitos ao mover para segundo tab na tela
    // de filtro de pedidos.
    this.goToSecondTabFilter = function() {
        $('#tab2')
            .removeClass('d_n')
            .addClass('tab-pane');
        $('#lnkTab2').tab('show');
    }
}

var visual = new Visual();