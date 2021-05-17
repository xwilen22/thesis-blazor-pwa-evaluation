using System.Collections.Generic;
namespace pwa_blazor.Models
{
    public class NodeInstance
    {
        public int Data { get; set; }
        public List<NodeInstance> ChildNodes { get; set; }

        public NodeInstance(int data)
        {
            Data = data;
            ChildNodes = new List<NodeInstance>();
        }
        public void AddChild(int data)
        {
            ChildNodes.Add(new NodeInstance(data));
        }
        public void AddToData(int amount)
        {
            Data += amount;
        }
    }
}