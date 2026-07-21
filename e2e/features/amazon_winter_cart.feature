Feature: Gestion del carrito de productos de invierno

  Scenario: Agregar un calefactor y una manta al carrito
    Given que el usuario se encuentra en la pagina principal de Amazon
    When busca el producto "electric heater"
    And selecciona un producto disponible de los resultados
    And agrega el producto seleccionado al carrito
    And busca el producto "winter blanket"
    And selecciona un producto disponible de los resultados
    And agrega el producto seleccionado al carrito
    Then el carrito debe contener los dos productos seleccionados
    And el subtotal debe coincidir con la suma de los productos
