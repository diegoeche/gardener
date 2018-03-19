defmodule UART.Supervisor do
  # Automatically defines child_spec/1
  use Supervisor

  def start_link(arg) do
    Supervisor.start_link(__MODULE__, arg, name: __MODULE__)
  end

  def init(_arg) do
    children = [
      {Collector, []}
    ]
    # Send tick to collector every second
    # :timer.apply_interval(:timer.seconds(1), Collector, :tick, [])

    Supervisor.init(children, strategy: :one_for_one)
  end
end
