import {BlockMath} from '../components/Katex'

export default function Katex(props) {
    return (
      <div>
        <BlockMath math={props.instruction}/>
      </div>
    )
  }
  