const postApi = async(route: string, command: string) : Promise<{response: string, msg: string}> => {
    let result = await fetch(`http://localhost:8080${route}`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        code: command,
        }),
    });
    const {response, msg} = await result.json().then((data) => data);
    return {response, msg}
}

const getApi = async(route: string) : Promise<{response: string, msg: string}> => {
    let result = await fetch(`http://localhost:8080${route}`, {method: "GET"});
    const {response, msg} = await result.json().then((data) => data);
    return {response, msg}
}

export {
    postApi,
    getApi
}
