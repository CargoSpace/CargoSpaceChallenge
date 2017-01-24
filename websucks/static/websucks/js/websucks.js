$( document ).ready(function() {
    
    var Submission = function() {
        var self = this;
        self.submission_id = null
        self.problem_title = '';
        self.submission_state = ko.observable();
        self.created_at = '';
    };
    
    var ContestModel = function() {
        var self = this;
        self.admin_notification = ko.observable('');
        self.submissions = ko.observableArray();
        self.websucks = null;
        self.addReplaceSubmission = function(submission) {
        var found = false;
        for(var i = 0; i < self.submissions().length; i++){
            if(self.submissions()[i].submission_id == submission.id){
                self.submissions()[i].submission_state(submission.submission_state);
                found = true;
                return;
            }
        }
        if(!found){ self.submissions.push(submission); }
    };
    self.removeSubmission = function(submission) { 
        self.submissions.remove(submission) 
    };
        self.initSocket = function(user_id, contest_id){
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            if(ReconnectingWebSocket){
                self.websucks = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/socket/" + user_id + "/" + contest_id);
            }else{
                self.websucks = new WebSocket(ws_scheme + '://' + window.location.host + "/socket/" + user_id + "/" + contest_id);
            }
            var submissionsLoaded = false;
            self.websucks.onmessage = function(message) {
                var data = JSON.parse(message.data);
                console.log(data.response)
                if(data.messageType == 'submissions' && !submissionsLoaded){
                    self.populateSubmissions(data.response);
                    submissionsLoaded = true; //incase of reconnection
                }else{
                    if(data.messageType == 'submission'){
                        self.populateSubmission(data.response);
                    }
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
            	submission.submission_state(submissions[i].submission_state);
            	submission.created_at = new Date(submissions[i].created_at).toLocaleString();
            	self.addReplaceSubmission(submission);
			}
        }
        
        self.populateSubmission = function(_submission){
			    var submission = new Submission();
			    submission.submission_id = _submission.id;
			    submission.submission_state(_submission.submission_state);
            	submission.problem_title = _submission.problem.title;
            	submission.created_at = new Date(_submission.created_at).toLocaleString();
            	self.addReplaceSubmission(_submission);
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

        