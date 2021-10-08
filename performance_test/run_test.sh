TEST_NAME=$1

yarn build

docker run \
  --network performance_test_default \
  --volume $PWD/build:/tests \
  -i loadimpact/k6 \
  run /tests/$TEST_NAME.js
