$(function() {
    var $story        = $('#story'),
        $table        = $('#table'),
        $question     = $('#question'),
        $answer       = $('#answer'),
        $getAnswer    = $('#get_answer'),
        $getStory     = $('#get_story'),
        $dis_question = $('#dis_question'),
        $explainTable = $('#explanation');

    getStory();

    // Activate tooltip
    $('.qa-container').find('.glyphicon-info-sign').tooltip();

    $getAnswer.on('click', function(e) {
        e.preventDefault();
        getAnswer();
    });

    $getStory.on('click', function(e) {
        e.preventDefault();
        getStory();
    });

    function getStory() {
        $.get('/get/story', function(json) {
            $story.val(json["story"]);

            // erase disambiguated query info
            $dis_question.html("");

            // Populate input table
            var tableHtml = [];
            var currentRow = '';
            var sentenceList = json["story"].split('\n');
            console.log(sentenceList)
            // var maxLatestSents = memProbs.length;
            var numSents = sentenceList.length;

            // start writing the first row of the table
            var rowHtml = [];
            rowHtml.push('<tr>');

            // iterate over rows
            for (var i = 0; i < numSents; i++) {
                // console.log(sentenceList[i])

                
                var cellList = sentenceList[i].split(' ');
                if (cellList[0] != currentRow){
                    // switch to the new row
                    rowHtml.push('</tr>');
                    tableHtml.push(rowHtml.join('\n'));
                    currentRow = cellList[0]
                    rowHtml = [];
                    rowHtml.push('<tr>');
                }
                // var row = cellList[0]
                // for (var j = 0; j < cellList.length; j++) {
                // if (cellList[0] == row) {
                rowHtml.push('<td>' + cellList[2] + '</td>');
                // }
                // for (var j = 0; j < 3; j++) {
                //     var val = memProbs[i][j].toFixed(2);
                //     if (val > 0) {
                //         rowHtml.push('<td style="color: black; ' +
                //             'background-color: rgba(97, 152, 246, ' + val + ');">' + val + '</td>');
                //     } else {
                //         rowHtml.push('<td style="color: black;">' + val + '</td>');
                //     }
                // }
                
            }
            // write the last row
            rowHtml.push('</tr>');
            tableHtml.push(rowHtml.join('\n'));

            $table.find('tbody').html(tableHtml);

            $question.val(json["question"]);
            $question.data('question_idx', json["question_idx"]);
            $question.data('suggested_question', json["question"]); // Save suggested question
            $answer.val('');
            $answer.data('correct_answer', json["correct_answer"]);
            //$explainTable.find('tbody').empty();
        });
    }

    function getAnswer() {
        var questionIdx       = $question.data('question_idx'),
            correctAnswer     = $answer.data('correct_answer'),
            suggestedQuestion = $question.data('suggested_question'),
            table             = $table.val(),
            question          = $question.val();

        var userQuestion = suggestedQuestion !== question? question : '';
        var url = '/get/answer?question_idx=' + questionIdx +
            '&user_question=' + encodeURIComponent(userQuestion);

        $.get(url, function(json) {
            var predAnswer = json["pred_answer"],
                dis_question = json["dis_question"],
                predProb = json["pred_prob"],
                memProbs = json["memory_probs"];
            console.log(dis_question)
            // $dis_question.val(dis_question);
            $dis_question.html(dis_question);

            var outputMessage = "Answer = '" + predAnswer + "'" +
                "\nConfidence score = " + (predProb * 100).toFixed(2) + "%";

            // Show answer's feedback only if suggested question was used
            if (userQuestion === '') {
                if (predAnswer === correctAnswer)
                    outputMessage += "\nCorrect!";
                else
                    outputMessage += "\nWrong. The correct answer is '" + correctAnswer + "'";
            }
            $answer.val(outputMessage);

            // Explain answer
            var explanationHtml = [];
            var sentenceList = $story.val().split('\n');
            var numSents = sentenceList.length;
            var maxLatestSents = memProbs.length;

            for (var i = Math.max(0, numSents - maxLatestSents); i < numSents; i++) {
                var rowHtml = [];
                rowHtml.push('<tr>');
                rowHtml.push('<td>' + sentenceList[i] + '</td>');
                for (var j = 0; j < 3; j++) {
                    var val = memProbs[i][j].toFixed(2);
                    if (val > 0) {
                        rowHtml.push('<td style="color: black; ' +
                            'background-color: rgba(97, 152, 246, ' + val + ');">' + val + '</td>');
                    } else {
                        rowHtml.push('<td style="color: black;">' + val + '</td>');
                    }
                }
                rowHtml.push('</tr>');
                explanationHtml.push(rowHtml.join('\n'));
            }
            $explainTable.find('tbody').html(explanationHtml);

            // Populate input table
            // var tableHtml = [];
            // var currentRow = '';
            // var sentenceList = json["story"].split('\n');
            // // var maxLatestSents = memProbs.length;
            // var numSents = sentenceList.length;
            // // start writing the first row of the table
            // var rowHtml = [];
            // rowHtml.push('<tr>');

            // // iterate over rows
            // for (var i = 0; i < numSents; i++) {
            //     // console.log(sentenceList[i])

                
            //     var cellList = sentenceList[i].split(' ');
            //     if (cellList[0] != currentRow){
            //         // switch to the new row
            //         rowHtml.push('</tr>');
            //         tableHtml.push(rowHtml.join('\n'));
            //         currentRow = cellList[0]
            //         rowHtml = [];
            //         rowHtml.push('<tr>');
            //     }
            //     // var row = cellList[0]
            //     // for (var j = 0; j < cellList.length; j++) {
            //     // if (cellList[0] == row) {
            //     var val = memProbs[i][0].toFixed(2);
            //     console.log(val)
            //     // rowHtml.push('<td>' + cellList[2] + '</td>');

            //     // for (var j = 0; j < 3; j++) {
            //     if (val > 0) {
            //         rowHtml.push('<td style="color: black; ' +
            //             'background-color: rgba(97, 152, 246, ' + val + ');">' + cellList[2] + '</td>');
            //     } else {
            //         rowHtml.push('<td style="color: black;">' + cellList[2] + '</td>');
            //     }
            //     // }

            //     // }
            //     // for (var j = 0; j < 3; j++) {
            //     //     var val = memProbs[i][j].toFixed(2);
            //     //     if (val > 0) {
            //     //         rowHtml.push('<td style="color: black; ' +
            //     //             'background-color: rgba(97, 152, 246, ' + val + ');">' + val + '</td>');
            //     //     } else {
            //     //         rowHtml.push('<td style="color: black;">' + val + '</td>');
            //     //     }
            //     // }
                
            // }
            // // write the last row
            // rowHtml.push('</tr>');
            // tableHtml.push(rowHtml.join('\n'));

            // $table.find('tbody').html(tableHtml);
        });
    }
});
