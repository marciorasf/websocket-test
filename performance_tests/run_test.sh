TEST_NAME=$1

yarn build

docker run \
  -- user 0 \
  --network performance_tests_default \
  --volume $PWD/build:/tests \
  --volume $PWD/output:/output \
  -i loadimpact/k6 \
  run --summary-export=/output/result.json /tests/$TEST_NAME.js
