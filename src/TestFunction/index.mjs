// index

export const handler = async (event) => {
  const html = `
    <html>
        <head>
            <title>xlk subsidiary</title>
        </head>
        <body>
            <p>This site is powered by AWS Lambda</p>
            <p>Current Time: ${new Date().toLocaleString()}</p>
        </body>
    </html>
  `;

  const response = {
    statusCode: 200,
    headers: {
      'content-type': 'text/html'
    },
    body: html,
  };

  return response;
};
