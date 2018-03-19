defmodule Collector do
  use GenServer

  def start_link(state) do
    GenServer.start_link(__MODULE__, state, name: __MODULE__)
  end

  ## Callbacks

  def init(stack) do
    {:ok, pid} = Nerves.UART.start_link
    Nerves.UART.open(pid, "ttyACM0", speed: 57600, active: true)
    Nerves.UART.configure(pid, framing: {Nerves.UART.Framing.Line, separator: "\r\n"})
    {:ok, stack}
  end

  def handle_info({:nerves_uart, "ttyACM0", amount}, state) do
    {:noreply, state}
  end

  def tick() do
    IO.puts(".")
  end

  def handle_call(:pop, _from, [h | t]) do
    {:reply, h, t}
  end

  def handle_cast({:push, h}, t) do
    {:noreply, [h | t]}
  end
end
