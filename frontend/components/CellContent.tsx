import React, {useState, useEffect} from "react";
import Katex from "./Katex";

const textareaStyle = {
    width: '100%',
    border: '1px solid black',
    overflow: 'hidden'
}

interface CellContentProp {
    content: string;
    setContent: Function;
    editorEnabled: boolean;
    setEditorEnabled: Function;
    executeAction: Function;
}

const CellContent = ({content, setContent, editorEnabled, setEditorEnabled, executeAction}: CellContentProp) => {
    const textareaRef = React.createRef<HTMLTextAreaElement>()

    useEffect(()=>{
        if(textareaRef?.current) textareaRef.current.focus()
    }, [textareaRef, content])

    return (
        <div>
            <div className="cursor-pointer" onClick={() => setEditorEnabled(!editorEnabled)}>
                { <Katex instruction={content} /> }
            </div>
            { (editorEnabled) &&
                <textarea
                    ref={textareaRef}
                    value={content} 
                    style={textareaStyle}
                    onKeyDown={(e) => {
                        if(e.code == "Enter" && e.shiftKey){
                            executeAction();
                            e.preventDefault()
                        }
                    }}
                    onInput={(e) => {
                        // black magic to make the textarea automatically resize on user input
                        const el = e.currentTarget
                        el.style.height = 'auto'
                        el.style.height = `${el.scrollHeight}px`
                        setContent(e.currentTarget.value)
                        console.log(content)
                    }} 
                />
            }
        </div>
    )
}


export default CellContent;
