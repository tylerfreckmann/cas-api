console.log("loaded");
Dropzone.options.myAwesomeDropzone = {
	init: function() {
		this.on("success", function(file, response) {
			console.log(response);
			$( "#image-demo" ).replaceWith(response)
		});
	}
};
