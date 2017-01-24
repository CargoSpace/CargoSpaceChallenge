$( document ).ready(function() {
    
    var Submission = function() {
        var self = this;
        self.submission_id = null
        self.problem_title = '';
        self.submission_state = ko.observable('PENDING');
        self.created_at = '';
    };
    
    var ContestModel = function() {
        var self = this;
        self.admin_notification = ko.observable('');
        self.submissions = ko.observableArray();
        self.websucks = null;
        self.addSubmission = function(submision) {
        	var submisionExists = false;
        	$.map(self.submissions(), function(tmpsubmision) {
        		if(tmpsubmision.submission_id == submision.id){
        			submisionExists = true;
        			return;
        		};
        	});
        	if(!submisionExists){
        	    self.submissions.push(submision);
        	}
        };
        self.initSocket = function(user_id, contest_id){
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            self.websucks = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/socket/" + user_id + "/" + contest_id);
            self.websucks.onmessage = function(message) {
                var data = JSON.parse(message.data);
                console.log(data);
                if(data.messageType == 'submissions'){
                    self.populateSubmissions(data.response);
                }else{
                    
                }
            };
            self.websucks.onopen = function() {
                this.send('Hello, channel ' + this.channel + ', from id: ' + this.id);
            }
        };
        self.populateSubmissions = function(submissions){
            
            for (var i = 0; i < submissions.length; i++){
			    var submission = new Submission();
			    submission.submission_id = submissions[i].id;
            	submission.problem_title = submissions[i].problem.title;
            	submission.created_at = new Date(submissions[i].created_at).toLocaleString();
            	self.addSubmission(submission);
			}
        }
    }
    
    if(user_id && contest_id && user_id.length > 0 && contest_id.length > 0){
        var contetModel = new ContestModel();
        ko.applyBindings(contetModel);
        contetModel.initSocket(user_id, contest_id);
    }else{
        console.log("Requirements to initiate sucket not met");
    }
    
});

        