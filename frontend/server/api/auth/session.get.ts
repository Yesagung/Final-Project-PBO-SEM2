const extractToken = (authHeaderValue: string) => {
    const [, token] = authHeaderValue.split(`Bearer `)
    return token
}

export default eventHandler(async (event) => {
    const authHeaderValue = getRequestHeader(event, 'authorization');

    if (!authHeaderValue) {
        throw createError({ statusCode: 403, statusMessage: 'You must be logged in to use this endpoint' })
    }
    const extractedToken = extractToken(authHeaderValue);
    let dataToken = JSON.parse(Buffer.from(extractedToken.split(".")[1], "base64").toString("utf-8"));
    dataToken.token = extractedToken;

    if (dataToken.exp > (Date.now() / 1000)) {
        return dataToken;
    }

    throw createError({ statusCode: 403, statusMessage: 'You must be logged in to use this endpoint' })
})
