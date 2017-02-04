$( document ).ready(function() {
    
    var Submission = function() {
        var self = this;
        self.submission_id = null
        self.problem_title = '';
        self.submission_state = ko.observable();
        self.created_at = '';
    };
    
    var UserSubmission = function() {
        var self = this;
        self.user = ''
        self.submission_id = null
        self.problem_title = '';
        self.submission_state = ko.observable();
        self.created_at = '';
    };
    
    var ContestModel = function() {
        var self = this;
        self.admin_notification = ko.observable('');
        self.submissions = ko.observableArray();
        self.all_submissions = ko.observableArray();
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
        self.addReplaceUserSubmission = function(userSubmission) {
            var found = false;
            for(var i = 0; i < self.all_submissions().length; i++){
                if(self.all_submissions()[i].submission_id == userSubmission.id){
                    self.all_submissions()[i].submission_state(userSubmission.submission_state);
                    found = true;
                    return;
                }
            }
            if(!found){ self.all_submissions.unshift(userSubmission); }
        };
        self.removeUserSubmission = function(userSubmission) {
            self.all_submissions.remove(userSubmission) 
        };
        self.initSocket = function(contest_id, user_id){
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            if(ReconnectingWebSocket){
                if(user_id && contest_id){
                    self.websucks = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/socket/" + contest_id + "/" + user_id);
                }else if(contest_id){
                    self.websucks = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/socket/" + contest_id + "/");
                }else{
                    throw new Error("Supply at least contest_id");
                }
            }else{
                if(user_id && contest_id){
                    self.websucks = new WebSocket(ws_scheme + '://' + window.location.host + "/socket/" + contest_id + "/" + user_id);
                }else if(contest_id){
                    self.websucks = new WebSocket(ws_scheme + '://' + window.location.host + "/socket/" + contest_id + "/");
                }else{
                    throw new Error("Supply at least contest_id");
                }
            }
            
            self.websucks.onmessage = function(message) {
                var data = JSON.parse(message.data);
                console.log(data.response)
                if(data.messageType == 'submissions'){
                    self.submissions.removeAll()
                    self.populateSubmissions(data.response);
                }else{
                    if(data.messageType == 'submission'){
                        self.populateSubmission(data.response);
                    }
                }
                if(data.messageType == 'all_submissions'){
                    self.all_submissions.removeAll()
                    self.populateUserSubmissions(data.response);
                }else{
                    if(data.messageType == 'new_submission'){
                        self.populateUserSubmission(data.response);
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
            	self.addReplaceSubmission(submission);
        }
        
        self.populateUserSubmissions = function(userSubmissions){
            
            for (var i = 0; i < userSubmissions.length; i++){
			    var userSubmission = new UserSubmission();
			    userSubmission.user = userSubmissions[i].submitted_by.first_name;
			    userSubmission.submission_id = userSubmissions[i].id;
            	userSubmission.problem_title = userSubmissions[i].problem.title + ' - ' + userSubmissions[i].problem.problem_type;
            	userSubmission.submission_state(userSubmissions[i].submission_state);
            	userSubmission.created_at = new Date(userSubmissions[i].created_at).toLocaleString();
            	self.addReplaceUserSubmission(userSubmission);
			}
        }
        
        self.populateUserSubmission = function(_submission){
			    var userSubmission = new UserSubmission();
			    userSubmission.user = _submission.submitted_by.first_name;
			    userSubmission.submission_id = _submission.id;
			    userSubmission.submission_state(_submission.submission_state);
            	userSubmission.problem_title = _submission.problem.title + ' - ' + _submission.problem.problem_type;
            	userSubmission.created_at = new Date(_submission.created_at).toLocaleString();
            	self.addReplaceUserSubmission(userSubmission);
        }
    }
    
    if(user_id && contest_id && user_id.length > 0 && contest_id.length > 0){
        var contetModel = new ContestModel();
        ko.applyBindings(contetModel);
        contetModel.initSocket(contest_id, user_id);
    }else if(contest_id && contest_id.length > 0){
        var contetModel = new ContestModel();
        ko.applyBindings(contetModel);
        contetModel.initSocket(contest_id);
    }else{
        console.log("Requirements to initiate sucket not met");
    }
    
});