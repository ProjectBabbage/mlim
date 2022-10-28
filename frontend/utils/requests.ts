const callApi = async(command: string) : Promise<{response: string, msg: string}> => {
    let result = await fetch("http://localhost:8080/code/", {
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

export {
    callApi
}
