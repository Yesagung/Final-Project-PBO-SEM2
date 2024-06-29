const runtimeConfig = useRuntimeConfig()

export default defineEventHandler(async (event) => {
    const body = await readBody(event);
    const loginPath = "/api/v1/login";
    const host = runtimeConfig.api.authUrl || "ipcam-be-service:5000";
    const url = "http://" + host + loginPath;
    return await fetch(url, {
        method: "POST",
        body: JSON.stringify({
            username: body.username,
            password: body.password
        }),
        headers: new Headers({
            "Content-Type": "application/json",
        }),
    })
        .then(async (res) => {
            let result: { token: string, detail: string } = await res.json();
            if (!res.ok) {
                throw createError({ statusCode: 403, statusMessage: result.detail })
            }
            return result;
        })
        .catch((error) => {
            console.log(error)
        })

})