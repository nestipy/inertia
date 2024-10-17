import { useState } from "react";
import { Link } from '@inertiajs/react'

type Props = {
    message: string,
    messages: any,
    lazy_prop: string
}
const Index = ({message, messages, lazy_prop}: Props) => {
    const [counter, setCounter] = useState<number>(0)
    return <main>
        <Link href="/2">Link to other page</Link>
        <Link href="/" only={['lazy_prop']}>Partial reload (only lazy prop)</Link>
        <button onClick={() => setCounter(p => p + 1)}>
            Reactive button (clicked {counter} times)
        </button>
        <div className="props">
            <h1>Props</h1>
            <span> Message: {message} </span>
            <span> Flashed messages: {JSON.stringify(messages)} </span>
            <span> Lazy prop: {lazy_prop} </span>
        </div>
    </main>
}

export default Index
