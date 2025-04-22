function toggleSearch(event: HTMLElement) {
    const parent: HTMLElement = event.parentElement!
    const children: HTMLCollection  = parent.children
    const serachMenu = children[0]
    const toggleBar = children[1]

    if (serachMenu.classList.contains("hidden")) {
        parent.classList.add("w-full")
        parent.classList.remove("w-5")
        serachMenu.classList.remove("hidden")
    } else {
        parent.classList.add("w-5")
        parent.classList.remove("w-full")
        serachMenu.classList.add("hidden")        
    }
}