DIR=$(cd "$(dirname "$0")"; pwd)

docker run \
--detach \
--user neo4j \
--publish=7474:7474 \
--publish=7687:7687 \
--volume=$DIR/neo4j/input:/input \
--env=NEO4J_AUTH=none \
--env=NEO4J_dbms_read__only=true \
--env=EXTENSION_SCRIPT=/input/extension_script.sh \
neo4j