__author__ = 'leif'
import os
import sys
import logging
import logging.config
import logging.handlers
from ifind.common.rotation_ordering import PermutatedRotationOrdering

work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, "data/smallindex")
my_whoosh_query_index_dir = os.path.join(work_dir,"/trec_query_index/index")
my_experiment_log_dir = work_dir
qrels_file =  os.path.join(work_dir, "data/TREC2005.qrels.txt")

print "Work DIR: " + work_dir
print "QRELS File: " + qrels_file
print "my_whoosh_doc_index_dir: " + my_whoosh_doc_index_dir

event_logger = logging.getLogger('event_log')
event_logger.setLevel(logging.INFO)
event_logger_handler = logging.FileHandler(os.path.join(my_experiment_log_dir, 'experiment.log' ) )
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)

# workflow must always start with /treconomics/startexperiment/

exp_work_flows = [
['/treconomics/startexperiment/','/treconomics/preexperiment/UK/','/treconomics/demographicssurvey/','/treconomics/searchefficacysurvey/','/treconomics/pretaskquestions/1/','/treconomics/search/1/','/treconomics/posttaskquestions/1/','/treconomics/pretaskquestions/2/','/treconomics/search/2/','/treconomics/posttaskquestions/2/','/treconomics/pretaskquestions/3/','/treconomics/search/3/','/treconomics/posttaskquestions/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/US/','/treconomics/demographicssurvey/','/treconomics/searchefficacysurvey/','/treconomics/pretaskquestions/1/','/treconomics/search/1/','/treconomics/posttaskquestions/1/','/treconomics/pretaskquestions/2/','/treconomics/search/2/','/treconomics/posttaskquestions/2/','/treconomics/pretaskquestions/3/','/treconomics/search/3/','/treconomics/posttaskquestions/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/US/','/treconomics/search/1/','/treconomics/search/2/','/treconomics/search/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/UK/','/treconomics/search/1/','/treconomics/search/2/','/treconomics/search/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/UK/','/treconomics/pretask/1/','/treconomics/search/1/','/treconomics/pretask/2/','/treconomics/search/2/','/treconomics/pretask/3/','/treconomics/search/3/','/treconomics/performance/','/treconomics/logout/']
]

class ExperimentSetup(object):

    def __init__(self, workflow, timeout = 660, topics=['999','347','344'], rpp=10, engine=1, interface=1, description=''):
        self.timeout = timeout
        self.topics = topics
        self.rpp = rpp
        self.engine = engine
        self.description = description
        self.workflow = workflow
        self.pro = PermutatedRotationOrdering()
        self.n =self.pro.number_of_orderings(self.topics)

    def _get_check_i(self, i):
        return i % self.n

    def get_rotations(self, i):
        """ get the ith rotation from the topics
        :param i:
        :return: returns the list of topic numbers
        """
        ith = self._get_check_i(i)

        return self.pro.get_ordering(self.topics,ith)

    def get_rotation_topic(self,i,t):
        """ get the ith rotation and the tth topic
        :param i: integer
        :param t: integer
        :return: returns the topic number
        """
        ith = self._get_check_i(i)
        rotations = self.pro.get_ordering(self.topics,ith)
        return rotations[t]


    def __str__(self):
        return self.description

exp0 = ExperimentSetup(workflow= exp_work_flows[4], interface=0, description='structured condition')
exp1 = ExperimentSetup(workflow= exp_work_flows[4], interface=0, description='structured condition')
exp2 = ExperimentSetup(workflow= exp_work_flows[4], description='standard condition')
exp3 = ExperimentSetup(workflow= exp_work_flows[4], interface=2, description='suggestion condition')
exp4 = ExperimentSetup(workflow= exp_work_flows[4], rpp=3)
exp5 = ExperimentSetup(workflow= exp_work_flows[4], rpp=6)

# these correspond to conditions
experiment_setups = [exp0,exp1,exp2,exp3,exp4,exp5]

