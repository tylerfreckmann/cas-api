$("#image-results").hide();
$("#exit").hide();

function turnIntoArray(dictionary) {
  var array = [];
  $.each(dictionary, function(index, value) {
    array.push({classification: index, probability: value});
  });
  return array;
}

function sortScores(scores) {
  return scores.sort(function(a, b) {
    return b.probability - a.probability;
  });
}

Dropzone.autoDiscover = false;

$(function () {
  var myDropzone = new Dropzone("#my-awesome-dropzone");
  myDropzone.on("success", function(file, response) {
    console.log(response);
    $("#image-demo").hide();
    $("#image-preview img").attr("src", response.imgUrl);

    var scores = turnIntoArray(response.scores);
    scores = sortScores(scores);
    console.log(scores);

    var scoreDivs = [];
    $.each(scores, function(index, score) {
      console.log(score);
      var classification = score.classification.slice(9);
      
      var row = $(document.createElement("div"));
      row.addClass("ty-row ty-labels");

      var name = $(document.createElement("div"));
      name.addClass("name ty-labels");
      name.text(classification);

      var prob = $(document.createElement("div"));
      prob.addClass("score ty-labels");
      prob.text(Math.round(score.probability * 100) + "%");

      var bar = $(document.createElement("div"));
      bar.addClass("bar ty-labels");

      var meter = $(document.createElement("div"));
      meter.addClass("meter ty-labels");
      meter.css("width", prob.text());

      bar.append(meter);
      row.append(name, prob, bar);

      scoreDivs.push(row);
    });

    $("#score-card").append(scoreDivs);
    $("#image-results").show();
    $("#exit").show();
  });

  $("#exit").click(function() {
    $("#image-preview img").attr("src", "");
    $("#score-card").empty();
    $("#image-results").hide();
    myDropzone.removeAllFiles();
    $("#image-demo").show();
    $("#exit").hide();
  });
});

