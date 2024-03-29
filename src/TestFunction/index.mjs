// index

export const handler = async (event) => {

  const userAgent = event.headers['User-Agent'] || event.headers['user-agent'];

  if(userAgent && userAgent.startsWith('curl/')) {
    return {
      statusCode: 200,
      headers: {
        'content-type': 'application/json'
      },
      body: JSON.stringify({ currDatetime: new Date().toISOString()})
    }
  } else {
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

  return {
    statusCode: 200,
    headers: {
      'content-type': 'text/html'
    },
    body: html,
  };
  }
};

//