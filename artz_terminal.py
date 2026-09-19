from datetime import datetime
import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.prompt import Prompt
from rich.text import Text

console = Console()
ACCENT = "bright_cyan"
GREEN = "bright_green"
RED = "bright_red"
DIM = "grey50"

def header():
    t = Text()
    t.append("  A  ", style=f"bold {ACCENT} on black")
    t.append(" ARTZ", style="bold white")
    t.append("  //  DARK FANTASY COMMAND NODE", style=DIM)
    t.append(f"    {datetime.now():%H:%M:%S}", style=GREEN)
    return Panel(t, border_style="grey30", padding=(0, 1))

def profile_panel():
    text = Text()
    text.append("\n       ◉\n", style=f"bold {ACCENT}")
    text.append("      ARTZ\n", style="bold white")
    text.append("  PROTAGONIST / OPERATOR\n\n", style=DIM)
    text.append("LEVEL       ", style=DIM); text.append("27\n", style="bold white")
    text.append("CLASS       ", style=DIM); text.append("VOID WARDEN\n", style=ACCENT)
    text.append("STATUS      ", style=DIM); text.append("ACTIVE\n", style=GREEN)
    text.append("\nSYNC        "); text.append("87%\n", style=GREEN)
    text.append("CORE        "); text.append("64%", style=ACCENT)
    return Panel(text, title="[bold]PROFILE // 01[/]", border_style="grey30")

def world_panel():
    text = Text()
    text.append("\n     ╱╲   ╱╲\n", style=DIM)
    text.append("   ╱█████╲╱██╲\n", style=ACCENT)
    text.append("  █  NOCTIS  █\n", style="white")
    text.append("   ╲██╱╲██╱\n\n", style=DIM)
    text.append("REGION     "); text.append("NOCTIS\n", style="white")
    text.append("THREAT     "); text.append("ELEVATED\n", style=RED)
    text.append("QUESTS     "); text.append("04 ACTIVE\n", style=ACCENT)
    text.append("SYNC       "); text.append("ONLINE", style=GREEN)
    return Panel(text, title="[bold]WORLD STATE // 02[/]", border_style="grey30")

def mission_panel():
    text = Text()
    text.append("THE VEIL IS OPEN\n", style="bold white")
    text.append("Investigate the corrupted gate beneath the old fortress.\n\n", style=DIM)
    text.append("PROGRESS  ")
    text.append("██████████████░░░░░░  ", style=ACCENT)
    text.append("72%", style=GREEN)
    text.append("\nREWARD    1,250 XP", style=DIM)
    return Panel(text, title="[bold]MISSION // 03[/]", border_style="grey30")

def network_panel():
    text = Text("NETWORK   ", style=DIM)
    text.append("●", style=GREEN)
    text.append("──●──●──●──", style=DIM)
    text.append("●", style=GREEN)
    text.append("  5 NODES / STABLE", style=DIM)
    return Panel(text, title="[bold]NETWORK // 04[/]", border_style="grey30")

def terminal_panel(lines):
    body = Text()
    for line in lines[-13:]:
        body.append(line + "\n")
    body.append("\n> ", style=ACCENT)
    body.append("Type ", style=DIM)
    body.append("help", style="bold white")
    body.append(" for commands.", style=DIM)
    return Panel(body, title="[bold]FSOCIETY TERMINAL // ARTZ[/]", border_style=ACCENT)

def build_screen(lines):
    layout = Layout()
    layout.split_column(Layout(header(), size=3), Layout(name="main", ratio=1), Layout(name="bottom", size=8))
    layout["main"].split_row(Layout(profile_panel(), size=27), Layout(terminal_panel(lines), ratio=1), Layout(world_panel(), size=31))
    layout["bottom"].split_row(Layout(mission_panel(), ratio=2), Layout(network_panel(), ratio=1))
    return layout

def run_command(cmd, history):
    c = cmd.lower().strip()
    history.append(f"[{datetime.now():%H:%M:%S}] > {cmd}")
    responses = {
        "help": ["AVAILABLE COMMANDS:", "  help     show commands", "  status   system status", "  profile  protagonist profile", "  world    current world state", "  mission  active mission", "  clear    clear terminal", "  exit     shutdown interface"],
        "status": ["ARTZ CORE ........ ONLINE", "VOID SYNC ........ 87%", "NETWORK .......... STABLE", "THREAT ........... ELEVATED"],
        "profile": ["NAME ............. ARTZ", "CLASS ............ VOID WARDEN", "LEVEL ............ 27", "STATUS ........... ACTIVE"],
        "world": ["REGION ........... NOCTIS", "QUESTS ........... 04 ACTIVE", "GATE STATUS ...... CORRUPTED", "OBJECTIVE ........ THE VEIL IS OPEN"],
        "mission": ["MISSION .......... THE VEIL IS OPEN", "PROGRESS ......... 72%", "REWARD ........... 1,250 XP"],
    }
    if c == "clear":
        history.clear()
        return False
    if c in responses:
        history.extend(responses[c])
    elif c:
        history.append("UNKNOWN COMMAND. Type 'help' to display commands.")
    return c == "exit"

def main():
    history = [
        "[22:50:01] Initializing ARTZ command interface...",
        "[22:50:02] Identity verified: ARTZ",
        "[22:50:03] Loading dark-fantasy world state...",
        "[22:50:04] All core systems operational.",
    ]
    console.clear()
    with Live(build_screen(history), console=console, refresh_per_second=8, screen=True) as live:
        while True:
            cmd = Prompt.ask("[bright_cyan]>[/]", console=console)
            should_exit = run_command(cmd, history)
            live.update(build_screen(history))
            if should_exit:
                history.append("Shutting down ARTZ command interface...")
                live.update(build_screen(history))
                time.sleep(0.8)
                break

if __name__ == "__main__":
    main()
