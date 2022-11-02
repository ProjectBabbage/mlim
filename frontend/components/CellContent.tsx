import React, {useEffect, useRef} from "react";
import Katex from "./Katex";


const textareaStyle = {
    width: '100%',
    border: '1px solid black',
    overflow: 'hidden'
}

interface CellContentProp {
    content: string;
    editorEnabled: boolean;
    updateContent: Function;
    setEditorEnabled: Function;
    executeAction: Function;
}

const CellContent = ({content, updateContent, editorEnabled, setEditorEnabled, executeAction}: CellContentProp) => {
    const textareaRef = useRef<HTMLTextAreaElement>()
    // const textareaRef = React.createRef<HTMLTextAreaElement>()

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
                        updateContent(e.currentTarget.value)
                    }} 
                />
            }
        </div>
    )
}


export default CellContent;
