$(document).ready(function() {
    gasIndex = 0;
    $('#diveForm')
        // Add button click handler
        .on('click', '.addButton', function() {
            gasIndex++;
            var $template = $('#gasTemplate'),
                $clone    = $template
                                .clone()
                                .removeClass('hide')
                                .removeAttr('id')
                                .attr('data-gas-index', gasIndex)
                                .insertBefore($template);

            // Update the name attributes
            $clone
                .find('[name="oxygen"]').attr('name', 'gas[' + gasIndex + '].oxygen').end()
                .find('[name="helium"]').attr('name', 'gas[' + gasIndex + '].helium').end()
                .find('[name="depth"]').attr('name', 'gas[' + gasIndex + '].depth').end()
                .find('[name="travel_gas"]').attr('name', 'gas[' + gasIndex + '].travel_gas').end();
        })

        // Remove button click handler
        .on('click', '.removeButton', function() {
            var $row  = $(this).parents('.form-group'),
                index = $row.attr('data-gas-index');

            // Remove element containing the fields
            $row.remove();
        });
});
