#docker exec -u befi8957 -it webis-datascience-image-befi8957 bash -l -c 'cd; exec /opt/spark/bin/spark-submit   /home/yamenajjour/git/topic_ontologies/topic_modeling/model_corpus_args_me_cluster.py'
#docker exec -u befi8957 -it webis-datascience-image-befi8957 bash -l -c 'cd; exec /opt/spark/bin/spark-submit --deploy-mode cluster --py-files /home/yamenajjour/git/topic_ontologies/deploy/topic-ontologies-dep.zip --executor-memory 2G --driver-memory 4G /home/yamenajjour/git/topic_ontologies/topic_modeling/model_corpus_args_me_cluster.py'
import sys
sys.path.insert(0,"/home/yamenajjour/git/topic-ontologies/")
from pyspark.sql import SparkSession
import argument_esa_model.esa_top_n_terms

from conf.configuration import *
set_cluster_mode()
import sys
spark = SparkSession.builder.appName('topic-ontologies').config('master','yarn').getOrCreate()
args_me = spark.read.format('csv').option('header','true').option('delimiter',',')
spark_context= spark.sparkContext
log4jLogger = spark_context._gateway.jvm.org.apache.log4j
LOGGER = log4jLogger.LogManager.getLogger(__name__)



URI = spark_context._gateway.jvm.java.net.URI
Path = spark_context._gateway.jvm.org.apache.hadoop.fs.Path
FileSystem = spark_context._gateway.jvm.org.apache.hadoop.fs.FileSystem
FsPermission = spark_context._gateway.jvm.org.apache.hadoop.fs.permission.FsPermission
fs = FileSystem.get(URI("hdfs://betaweb020.medien.uni-weimar.de:8020"), spark_context._jsc.hadoopConfiguration())
fs.listStatus(Path('/user/befi8957'))


def get_vocab_size(model):
    if '-' in model:
        vocab_size=int(model.split("-")[-1])
    else:
        vocab_size=10
    return vocab_size

def dict_to_list(dictionary):
    vector  = []
    for key in sorted(dictionary):
        vector.append(dictionary[key])
    return vector

def project_documents(topic_ontology,model,is_testing):
    vocab_size = get_vocab_size(model)
    LOGGER.warn("Lok: vocab size %d"%vocab_size)
    def project_document(argument):
        if is_testing:
            return dict_to_list({"a":0.3,"b":0.3,"c":0.4})
        import nltk
        nltk.data.path.append('/mnt/ceph/storage/data-in-progress/topic-ontologies/nltk/')
        set_cluster_mode()
        path_corpus = get_path_source("ontology-"+topic_ontology)
        path_word2vec_model = get_path_topic_model('word2vec','word2vec')
        path_word2vec_vocab = get_path_vocab('word2vec')
        vector = argument_esa_model.esa_top_n_terms.model_topic(path_corpus,path_word2vec_model,path_word2vec_vocab,argument,vocab_size)
        return dict_to_list(vector)

    path_corpus = get_path_source("ontology-"+topic_ontology)
    LOGGER.warn("Lok: topic ontology documents are here %s"%path_corpus)
    path_word2vec_model = get_path_topic_model('word2vec','word2vec')
    LOGGER.warn("Lok: word 2vec model is here %s"%path_word2vec_model)
    path_documents = get_path_preprocessed_documents('sample')
    LOGGER.warn("Lok: documents are at %s"%path_documents)
    path_document_vectors= get_path_document_vectors('sample',topic_ontology,model).replace(".csv","")
    LOGGER.warn("Lok: documents vectors are at %s"%path_document_vectors)
    documents_df  = spark.read.format("csv").option("header", "true").option("delimiter", ",", ).option('quote', '"').load(path_documents)
    LOGGER.warn("Lok: loaded %d documents"%documents_df.count())
    documents = documents_df.select("document").rdd.map(lambda r: r[0])
    ids = (documents_df.select("document-id").rdd.map(lambda r: r[0]))

    vectors = documents.map(lambda document:project_document(document))

    ids_with_vectors=vectors.zip(ids)

    FileSystem.mkdirs(fs,Path(path_document_vectors),FsPermission(77777))
    LOGGER.warn("Lok: created output directory at %s"%path_document_vectors)

    ids_with_vectors.saveAsPickleFile(path_document_vectors)
    LOGGER.warn("Lok: finished documents%s"%path_document_vectors)





model = sys.argv[2]
ontology = sys.argv[1]
LOGGER.warn("Lok: processing %s %s"%(model,ontology))
project_documents(ontology,model,False)
