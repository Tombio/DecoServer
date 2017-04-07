

$(document).ready(function() {
    gasIndex = 0;
    var test_data = JSON.stringify({
    	"gas_list": [
    		{"oxygen": 21, "helium": 40, "depth": 0, "travel_gas": false},
    		{"oxygen": 50, "helium": 0, "depth": 21, "travel_gas": false},
    		{"oxygen": 100, "helium": 0, "depth": 6, "travel_gas": false}
    	],
    	"dive_plan": {
    		"maximum_depth": 50,
    		"bottom_time": 50
    	},
    	"deco_model": {
    		"algorithm": "ZH_L16B_GF",
    		"gf_low": 30,
    		"gf_high": 90
    	}
    });

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
        })

        .on('submit',function(e){
            e.preventDefault();
            //ajax code here
            var depth = $('#dive_max_depth').val();
            var time = $('#dive_bottom_time').val();

            $.ajax({
                type : "POST",
                url : "deco",
                data : test_data,
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
                data : test_data,
                // #contentType : "application/json",
                success : function(response) {
                    console.log("Data Loaded: " + response);
                    deco_chart.load(response);
                },
                async : false
            });
        });
});
