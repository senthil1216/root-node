$(function(){
	$("#target-editor").markdown({
	  savable:true,
	  /*
	  onShow: function(e){
	    alert("Showing "
	      +e.$textarea.prop("tagName").toLowerCase()
	      +"#"
	      +e.$textarea.attr("id")
	      +" as Markdown Editor...")
	  },
	  */
	 
	  onPreview: function(e) {
	    var previewContent;

		/*
	    if (e.isDirty()) {
	      var originalContent = e.getContent()

	      previewContent = "Prepended text here..."
	             + "\n"
	             + originalContent
	             + "\n"
	             +"Apended text here..."
	    } else {
	      previewContent = "Default content"
	    }*/

	    previewContent = e.parseContent();

	    return previewContent
	  },
	  onSave: function(e) {
		$("#myForm").submit();
	  }
	})
})