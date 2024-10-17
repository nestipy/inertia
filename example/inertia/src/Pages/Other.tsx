import { FormEvent, useCallback } from "react";
import { Link, useForm } from '@inertiajs/react'

type Props = {
    message: string,
    messages: any,
}

type Login = {
    email: string,
    password: string
}
const Other = ({message, messages}: Props) => {
    const loginForm = useForm<Login>({
        email: '',
        password: ''
    })
    const submitForm = useCallback((e: FormEvent<HTMLElement>) => {
        e.preventDefault()
        loginForm.post('/login')
    }, [loginForm])

    return <main>
        <Link href="/">Link to other page</Link>
        <div className="props">
            <h1>Props</h1>
            <span> Message: {message} </span>
            <span> Flashed messages: {JSON.stringify(messages)} </span>
        </div>
        <form onSubmit={submitForm}>
            <input
                type="text"
                placeholder="email"
                value={loginForm.data.email}
                onChange={e => loginForm.setData({...loginForm.data, 'email': e.target.value})}/>
            {loginForm.errors.email && <div>{loginForm.errors.email}</div>}
            <input
                type="password"
                placeholder="password"
                onChange={e => loginForm.setData({...loginForm.data, 'password': e.target.value})}/>
            {loginForm.errors.password && <div>{loginForm.errors.password}</div>}

            <button
                type="submit"
                disabled={loginForm.processing}>Login
            </button>
        </form>
    </main>
}

export default Other
