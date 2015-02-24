$( document ).ready(function() {
    $("input[name='age']").keyup(function(){
    	var ageEntry = $("input[name='age']").val();
    	if (!($.isNumeric(ageEntry))){
            alert("Please enter a number for age.");
    		$("input[name='age']").val(parseInt(ageEntry));
    	};
    });
});