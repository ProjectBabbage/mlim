import { useEffect, useState } from "react";
import { KEYCODES, NON_PRINTABLE_KEYS } from "../constants/keys";
import Katex from "../pages/katex";

export default function REPL() {
    const [toggled, setToggled] = useState(false);
    const [content, setContent] = useState("")
    const [historyText, setHistoryText] = useState("")
    const [history, setHistory] = useState([])  // [ [is_command, content] ]
    const [historyIndex, setHistoryIndex] = useState(0)
    const [vars, setVars] = useState({})
    const [varsDisplay, setVarsDisplay] = useState([])

    useEffect(() => {
        let result = ""
        history.forEach((entry) => {
            if(entry[0])
                result += "$"+entry[1] + "\n"
            else
                result += "->"+entry[1] + "\n"
        })
        setHistoryText(result)
    }, [history.length])

    useEffect(() => {
        let newVars = []
        for(const [key, value] of Object.entries(vars)){
            console.log(key)
            console.log(value)
            newVars.push(<div key={key}>{key} : {value}</div>)
        }
        setVarsDisplay(newVars);
    }, [JSON.stringify(vars)])
    function toggleREPL(){
        setToggled(!toggled)
    }

    function clearHistoryIndex(){
        setHistoryIndex(history.length - 1)
    }

    async function callApi(command){
        let response = await fetch('http://localhost:8080/code/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'code': command
            })
        })
        let result = await response.json()
            .then(function(data) {
                setVars(data.STATE)
                return data.RESULT;
            });
        return result

    }

    async function handleKeyPressed(evt){
        let keyCode = evt.keyCode
        let key = evt.key

        if(toggled && !NON_PRINTABLE_KEYS.includes(keyCode)) {
            if(
                47 < keyCode && keyCode < 112 ||
                159 < keyCode && keyCode < 177 ||
                183 < keyCode && keyCode < 224 ||
                keyCode == KEYCODES.SPACE
            ) {
                setContent(content + key)
            } else if (keyCode === KEYCODES.BACKSPACE) {
                setContent(content.substring(0, content.length - 1))
            } else if (keyCode === KEYCODES.ENTER && content.length) {
                history.push([true, content])
                history.push([false, await callApi(content)])
                clearHistoryIndex()
                setContent("")
            } else if (keyCode === KEYCODES.ARROW_UP && history.length) {
                if(historyIndex > 0){
                    setContent(history[historyIndex - 1][1])
                    setHistoryIndex(historyIndex - 1)
                }
            } else if(keyCode === KEYCODES.ARROW_DOWN) {     // ARROW DOWN
                if(historyIndex < history.length - 1){
                    setContent(history[historyIndex + 1][1])
                    setHistoryIndex(historyIndex + 1)
                } else {
                    setContent("")
                    setHistoryIndex(history.length)
                }
            }
        }
    }

    return (
        <div>
            <div>
                <div>
                    Available vars ( use STATE["var_name"] )
                </div>
                {varsDisplay}
            </div>
            <div>
                <Katex instruction={content}/>
            </div>
        <div 
            className={`
            bg-slate-500 h-96 w-96 whitespace-pre-line
            ${toggled ? "border border-white " : " "} 
            `} 
            onClick={() => toggleREPL()}
            onKeyDown={(evt) => handleKeyPressed(evt)}
            tabIndex="0"
            >
        {historyText}{">"}{content}{toggled ? <div className="animate-pulse inline">|</div> : ""}
        </div>
        </div>
    )
}