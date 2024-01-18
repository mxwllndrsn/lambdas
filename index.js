// index

export const handler = async (event) => {
  // TODO implement
  let message = {
    response: 'hi hi hi',
    currDatetime: new Date()
  }
  let currDatetime = new Date();
  const response = {
    statusCode: 200,
    body: JSON.stringify(message),
  };
  return response;
};
