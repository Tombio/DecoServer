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
                .find('[name="oxygen:skip"]').attr('name', 'gas_list[' + gasIndex + '][oxygen]:number').end()
                .find('[name="helium:skip"]').attr('name', 'gas_list[' + gasIndex + '][helium]:number').end()
                .find('[name="depth:skip"]').attr('name', 'gas_list[' + gasIndex + '][depth]:number').end()
                .find('[name="travel_gas:skip"]').attr('name', 'gas_list[' + gasIndex + '][travel_gas]:boolean').end()
        })

        // Remove button click handler
        .on('click', '.removeButton', function() {
            var $row  = $(this).parents('.form-group'),
                index = $row.attr('data-gas-index');

            // Remove element containing the fields
            $row.remove();
        })

        .on('submit',function(e){
            e.preventDefault();

            var data = $('#diveForm').serializeJSON({
                checkboxUncheckedValue: "false",
                useIntKeysAsArrayIndex: true});

            console.log(JSON.stringify(data));

            $.ajax({
                type : "POST",
                url : "deco",
                data : JSON.stringify(data),
                // #contentType : "application/json",
                success : function(response) {
                    console.log("Deco data " + response)
                    $('#deco_table').bootstrapTable('load', response);
                    $('#deco_table').bootstrapTable('hideLoading');
                },
                async : false
            });

            $.ajax({
                type : "POST",
                url : "chart",
                data : JSON.stringify(data),
                // #contentType : "application/json",
                success : function(response) {
                    console.log("Data Loaded: " + response);
                    deco_chart.load(response);
                },
                async : false
            });
        });
});
